"""Push window metrics to Amazon CloudWatch.

Owner: Person 3 (publishers/AWS)
Status: SCAFFOLD, not implemented.

Planned:
- Enabled only when `settings.cloudwatch_enabled` is True.
- put_metric_data to `settings.cloudwatch_namespace` in `settings.aws_region`
  (honour `settings.aws_endpoint_url` for LocalStack).
- Credentials come from the standard AWS chain, never from code or .env.example.
"""
