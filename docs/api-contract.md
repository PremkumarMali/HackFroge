# API Contract

Shared contract between the backend (Person 2), WebSockets/integration
(Person 3), and the frontend (Person 1). **Change this file in a PR before
changing any payload.** The Pydantic mirror of these shapes lives in
[`backend/app/models/schemas.py`](../backend/app/models/schemas.py), and the two
must stay in sync.

| Endpoint          | Status          | Owner    |
|-------------------|-----------------|----------|
| `GET /health`     | **Implemented** | Person 2 |
| `GET /metrics`    | Planned         | Person 2 |
| `GET /alerts`     | Planned         | Person 2 |
| `WS /ws/metrics`  | Planned         | Person 3 |
| `WS /ws/alerts`   | Planned         | Person 3 |

## Conventions

- Base URL (local): `http://localhost:8000`, WebSocket: `ws://localhost:8000`
- All timestamps are ISO 8601 in **UTC** with a `Z` suffix, e.g. `2026-09-28T10:04:00Z`.
- JSON field names are `snake_case`.
- Errors use FastAPI's default shape: `{"detail": "..."}` (422 for invalid query params).

## Severity

Exactly four values, as uppercase strings:

| Value    | Meaning                                         | Default rule (anomaly score `s`) |
|----------|-------------------------------------------------|----------------------------------|
| `NORMAL` | Window is within the baseline. No alert.        | `s < 2.0`                        |
| `LOW`    | Mild deviation, worth watching.                 | `2.0 ≤ s < 3.0`                  |
| `MEDIUM` | Clear anomaly, investigate.                     | `3.0 ≤ s < 4.0`                  |
| `HIGH`   | Severe anomaly, page someone (SNS by default).  | `s ≥ 4.0`                        |

Thresholds are configurable (`SEVERITY_*_THRESHOLD`). While the baseline is
warming up (`baseline.ready == false`) severity is always `NORMAL`.

## Shared objects

### MetricsSnapshot

One closed sliding window.

```json
{
  "window_start": "2026-09-28T10:04:00Z",
  "window_end": "2026-09-28T10:05:00Z",
  "line_count": 118,
  "error_count": 31,
  "warn_count": 4,
  "error_rate": 0.2627,
  "baseline": {
    "ready": true,
    "line_count_mean": 120.4,
    "line_count_std": 8.2,
    "error_rate_mean": 0.012,
    "error_rate_std": 0.006
  },
  "anomaly_score": 41.8,
  "severity": "HIGH"
}
```

| Field           | Type     | Notes                                                    |
|-----------------|----------|----------------------------------------------------------|
| `window_start`  | datetime | Inclusive                                                |
| `window_end`    | datetime | Exclusive                                                |
| `line_count`    | int      | Parsed lines in the window                               |
| `error_count`   | int      | Lines with level `ERROR`                                 |
| `warn_count`    | int      | Lines with level `WARN`                                  |
| `error_rate`    | float    | `error_count / line_count`, `0.0` if no lines            |
| `baseline`      | object   | Stats values are `null` while `ready` is `false`         |
| `anomaly_score` | float    | ≥ 0. Higher is more anomalous (statistical: max z-score) |
| `severity`      | Severity |                                                          |

### Alert

Created for every window whose severity is not `NORMAL`.

```json
{
  "id": "6f1c2a9e-4b7d-4f0e-9a51-2d8c3e7b1a90",
  "created_at": "2026-09-28T10:05:00Z",
  "severity": "HIGH",
  "title": "Error rate spike",
  "description": "error_rate 0.263 vs baseline 0.012 ± 0.006 (score 41.8)",
  "metric": "error_rate",
  "observed": 0.2627,
  "expected": 0.012,
  "anomaly_score": 41.8,
  "window_start": "2026-09-28T10:04:00Z",
  "window_end": "2026-09-28T10:05:00Z",
  "detector": "statistical",
  "explanation": [
    "error_count rose from ~1.4 to 31 per window",
    "Top error: 'Database connection timeout after 5000ms' in payment-service"
  ],
  "sample_lines": [
    "2026-09-28 10:04:02,847 ERROR [payment-service] Database connection timeout after 5000ms"
  ]
}
```

| Field           | Type         | Notes                                                        |
|-----------------|--------------|--------------------------------------------------------------|
| `id`            | string       | UUID, unique per alert                                       |
| `created_at`    | datetime     |                                                              |
| `severity`      | Severity     | Never `NORMAL`                                               |
| `title`         | string       | Short, human readable                                        |
| `description`   | string       | One line with the numbers                                    |
| `metric`        | string       | Metric that triggered it, e.g. `error_rate`, `line_count`    |
| `observed`      | float        | Value in this window                                         |
| `expected`      | float        | Baseline mean                                                |
| `anomaly_score` | float        |                                                              |
| `window_start`  | datetime     |                                                              |
| `window_end`    | datetime     |                                                              |
| `detector`      | string       | `statistical` (core). Optional ML: `isolation_forest`, `deeplog` |
| `explanation`   | string[]     | May be empty                                                 |
| `sample_lines`  | string[]     | Up to 5 raw lines from the window. May be empty              |

## REST

### `GET /health`

**Implemented.** Liveness probe.

`200 OK`

```json
{"status": "ok", "service": "log-anomaly-detector"}
```

### `GET /metrics`

**Planned.** Latest window plus recent history.

| Query param | Type | Default | Notes            |
|-------------|------|---------|------------------|
| `limit`     | int  | `60`    | 1–1000 windows   |

`200 OK`

```json
{
  "current": { "...": "MetricsSnapshot" },
  "history": [ { "...": "MetricsSnapshot" } ]
}
```

- `current` is `null` until the first window closes.
- `history` is ordered **oldest → newest** (ready to plot) and includes `current`.

### `GET /alerts`

**Planned.** Recent alerts for the feed.

| Query param    | Type     | Default | Notes                                   |
|----------------|----------|---------|-----------------------------------------|
| `limit`        | int      | `50`    | 1–500                                   |
| `min_severity` | Severity | `LOW`   | Returns alerts at or above this level   |

`200 OK`

```json
{
  "alerts": [ { "...": "Alert" } ],
  "total": 12
}
```

- `alerts` is ordered **newest → oldest**.
- `total` is the number of stored alerts matching `min_severity` (before `limit`).

## WebSockets

Both sockets are **server → client push only**. Every message uses one envelope:

```json
{"type": "<message type>", "data": { ... }}
```

Clients should ignore unknown `type` values (forward compatible). Anything a
client sends is ignored. On disconnect, clients reconnect with backoff (1s, 2s,
4s, max 10s) and **backfill via the REST endpoint** before resuming.

### `WS /ws/metrics`

**Planned.** One message each time a window closes.

```json
{"type": "metrics", "data": { "...": "MetricsSnapshot" }}
```

### `WS /ws/alerts`

**Planned.** One message per new alert (severity `LOW` or above).

```json
{"type": "alert", "data": { "...": "Alert" }}
```
