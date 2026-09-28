"""In-memory store backing GET /metrics and GET /alerts.

Owner: Person 2 (backend detection/core/API)
Status: SCAFFOLD, not implemented.

Planned:
- Bounded ring buffers for recent MetricsSnapshot and Alert objects.
- In-memory is enough for the demo; persistence (e.g. SQLite) is optional.
"""
