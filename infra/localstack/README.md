# LocalStack (local AWS emulator)

**Owner:** Person 3

Lets us develop the CloudWatch and SNS publishers without a real AWS account.

## Start

```bash
docker compose --profile aws up
```

`init-aws.sh` runs automatically when LocalStack is ready and creates:

| Resource  | Name / ARN                                                   |
|-----------|--------------------------------------------------------------|
| SNS topic | `arn:aws:sns:us-east-1:000000000000:log-anomaly-alerts`      |

CloudWatch metric namespaces need no setup. They appear on the first
`put_metric_data` call.

## Point the backend at LocalStack

In `backend/.env`:

```
AWS_ENDPOINT_URL=http://localhost:4566   # backend on host
# AWS_ENDPOINT_URL=http://localstack:4566  # backend in docker compose
CLOUDWATCH_ENABLED=true
SNS_ENABLED=true
SNS_TOPIC_ARN=arn:aws:sns:us-east-1:000000000000:log-anomaly-alerts
```

boto3 still needs *some* credentials to sign requests. LocalStack accepts
dummy values, so export them in your shell only (never in a committed file):

```bash
export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test
```

The compose file passes these through from your shell if they are set.

## Notes

- The image is pinned to `localstack/localstack:3.8`. If you switch to a newer
  image that requires an auth token, export `LOCALSTACK_AUTH_TOKEN` in your
  shell. Compose passes it through, and it must never be committed.
- Shell scripts here must keep LF line endings (enforced by `.gitattributes`).
