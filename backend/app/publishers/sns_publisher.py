"""Send alert notifications via Amazon SNS.

Owner: Person 3 (publishers/AWS)
Status: SCAFFOLD, not implemented.

Planned:
- Enabled only when `settings.sns_enabled` is True and `settings.sns_topic_arn` is set.
- Publish only alerts with severity >= `settings.sns_min_severity`.
- Honour `settings.aws_endpoint_url` for LocalStack.
"""
