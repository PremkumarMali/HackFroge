"""Parse raw log lines into structured events.

Owner: Person 2 (backend detection/core)
Status: SCAFFOLD, not implemented.

Planned:
- Parse the format documented in docs/architecture.md#log-format
  (timestamp, level, service, message).
- Malformed lines are counted, never raised.
"""
