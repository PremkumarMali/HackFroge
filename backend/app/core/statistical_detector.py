"""Core statistical anomaly detector. This is the PRIMARY detector.

Owner: Person 2 (backend detection/core)
Status: SCAFFOLD, not implemented.

Planned:
- Score each closed window against the baseline (e.g. z-score on
  error_rate and line_count; take the max as `anomaly_score`).
- Return NORMAL while the baseline is warming up.
- Optional ML detectors in app/ml/ may only be added once this works end to end.
"""
