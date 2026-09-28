"""Map an anomaly score to a Severity (NORMAL, LOW, MEDIUM, HIGH).

Owner: Person 2 (backend detection/core)
Status: SCAFFOLD, not implemented.

Planned thresholds (from settings):
    score <  severity_low_threshold      -> NORMAL
    score <  severity_medium_threshold   -> LOW
    score <  severity_high_threshold     -> MEDIUM
    otherwise                            -> HIGH
"""
