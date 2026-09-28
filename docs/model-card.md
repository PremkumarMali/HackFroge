# Model Card: Log Anomaly Detector

**Status:** draft. Fill in the TBD sections as the detector is built and evaluated.
**Owners:** Person 2 (detector), Person 4 (evaluation & documentation)

## 1. Primary detector: rolling statistical baseline (required)

### What it does

For each closed time window it computes:

| Feature      | Definition                          |
|--------------|-------------------------------------|
| `line_count` | Number of parsed lines              |
| `error_rate` | `error_count / line_count`          |

Each feature is compared with a rolling baseline (mean and standard deviation
over the last `BASELINE_WINDOW_COUNT` non-anomalous windows):

```
z = |x - mean| / max(std, epsilon)
anomaly_score = max(z over features)
```

`anomaly_score` is mapped to `NORMAL / LOW / MEDIUM / HIGH` using the
thresholds in [`api-contract.md`](api-contract.md#severity).

### Why this first

- Works with no training data and no labelled incidents.
- Fully explainable ("error rate 0.26 vs normal 0.01").
- Cheap enough to run on every window in real time.

### Intended use

- Detecting sudden spikes/drops in log volume and error rate in a single
  service's application log, surfaced in a live alert feed.

### Out of scope / not intended for

- Security intrusion detection, root-cause analysis, or multi-host correlation.
- Slow drifts that happen gradually enough to be absorbed into the baseline.

### Known limitations

- **Warm-up:** no alerts until `BASELINE_WINDOW_COUNT` windows have been seen.
- **Seasonality:** no daily/weekly pattern modelling. Regular peaks may alert.
- **Low volume:** near-empty windows make `error_rate` noisy (1 error in 2 lines = 50%).
- **Baseline poisoning:** a long incident could shift the baseline if anomalous
  windows are not excluded.
- **Format dependence:** only lines matching the documented log format are counted.

### Evaluation plan

| Scenario                         | Injected via                          | Expected severity | Result |
|----------------------------------|---------------------------------------|-------------------|--------|
| Steady normal traffic            | `scripts/generate_logs.py`            | `NORMAL`          | TBD    |
| Error burst (e.g. DB timeouts)   | `scripts/inject_anomaly.py --kind error-burst`  | `MEDIUM`/`HIGH` | TBD |
| Volume spike                     | `scripts/inject_anomaly.py --kind volume-spike` | `MEDIUM`/`HIGH` | TBD |
| Volume drop (service goes quiet) | Stop the generator                    | `LOW`+            | TBD    |
| Warm-up period                   | Fresh start                           | `NORMAL`          | TBD    |

Metrics to report: detection delay (seconds from injection to alert),
false alerts per hour of normal traffic, and missed injections.

## 2. Optional detectors (stretch, not required)

Only started after section 1 passes the evaluation above.

| Detector          | Input                          | Status          |
|-------------------|--------------------------------|-----------------|
| Isolation Forest  | Window feature vectors         | Not implemented |
| DeepLog-style LSTM| Sequences of log keys/templates| Not implemented |

If built: document training data, features, hyperparameters, artifact location
(`backend/artifacts/`), and a side-by-side comparison with the statistical
detector on the same scenarios.

## 3. Ethical / operational considerations

- Logs may contain user identifiers. Do not ship raw log lines to third
  parties. `sample_lines` in alerts should be reviewed before enabling SNS to
  external subscribers.
- Alerts are decision support for an on-call engineer, not automated actions.
