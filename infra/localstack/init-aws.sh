#!/bin/bash
# Runs inside LocalStack once it is ready (mounted into /etc/localstack/init/ready.d/).
# Creates the local AWS resources the backend expects. No real AWS account is used.
set -euo pipefail

awslocal sns create-topic --name log-anomaly-alerts
