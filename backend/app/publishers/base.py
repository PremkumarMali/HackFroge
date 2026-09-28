"""Common publisher interface.

Owner: Person 3 (publishers/AWS)
Status: SCAFFOLD, not implemented.

Planned:
- publish_metrics(snapshot: MetricsSnapshot)
- publish_alert(alert: Alert)
- A failing publisher must log the error and never stop the pipeline.
"""
