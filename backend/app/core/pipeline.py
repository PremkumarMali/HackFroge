"""Wire the detection pipeline together as a background task.

Owner: Person 2 (core) + Person 3 (integration)
Status: SCAFFOLD, not implemented.

Planned flow (started from FastAPI lifespan):
    log_tailer -> log_parser -> sliding_window -> baseline
      -> statistical_detector -> severity_classifier
      -> alert_store + publishers (WebSocket, CloudWatch, SNS)
"""
