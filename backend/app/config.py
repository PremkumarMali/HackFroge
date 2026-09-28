"""Application settings.

Values are read from environment variables (case-insensitive) and from an
optional `backend/.env` file. See `backend/.env.example` for every key.

AWS credentials are intentionally NOT settings. boto3 resolves them through
the standard AWS credential chain (env vars, ~/.aws, IAM role).
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal, Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

SERVICE_NAME = "log-anomaly-detector"

# backend/app/config.py -> parents[2] is the repository root (or "/" in Docker).
_PROJECT_ROOT = Path(__file__).resolve().parents[2]


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Log ingestion -------------------------------------------------------
    log_file_path: Path = _PROJECT_ROOT / "data" / "app.log"
    poll_interval_seconds: float = 1.0

    # --- Sliding window / baseline -------------------------------------------
    window_size_seconds: int = 60
    baseline_window_count: int = 30

    # --- Severity thresholds (anomaly score, e.g. z-score) -------------------
    # Placeholders until the statistical detector is tuned.
    severity_low_threshold: float = 2.0
    severity_medium_threshold: float = 3.0
    severity_high_threshold: float = 4.0

    # --- AWS -----------------------------------------------------------------
    aws_region: str = "us-east-1"
    # Set to http://localhost:4566 (or http://localstack:4566 in Docker) for LocalStack.
    aws_endpoint_url: Optional[str] = None

    # --- CloudWatch ----------------------------------------------------------
    cloudwatch_enabled: bool = False
    cloudwatch_namespace: str = "LogAnomalyDetector"

    # --- SNS -----------------------------------------------------------------
    sns_enabled: bool = False
    sns_topic_arn: Optional[str] = None
    sns_min_severity: Literal["LOW", "MEDIUM", "HIGH"] = "HIGH"


@lru_cache
def get_settings() -> Settings:
    return Settings()
