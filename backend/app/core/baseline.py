"""Rolling baseline of "normal" window metrics.

Owner: Person 2 (backend detection/core)
Status: SCAFFOLD, not implemented.

Planned:
- Rolling mean/std over the last `settings.baseline_window_count` windows.
- `ready` is False until enough windows have been seen (warm-up).
- Anomalous windows should not pollute the baseline.
"""
