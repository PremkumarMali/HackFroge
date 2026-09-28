"""Aggregate parsed events into fixed time windows.

Owner: Person 2 (backend detection/core)
Status: SCAFFOLD, not implemented.

Planned:
- Window length: `settings.window_size_seconds`.
- Per window: line_count, error_count, warn_count, error_rate.
- Emit a closed window to the baseline/detector when time rolls over.
"""
