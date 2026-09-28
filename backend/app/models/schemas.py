"""Shared API schemas. Keep in sync with docs/api-contract.md.

Only HealthResponse is served today; the rest define the planned contract so
backend, WebSocket, and frontend work can proceed in parallel.
"""

from datetime import datetime
from enum import Enum
from typing import List, Literal, Optional

from pydantic import BaseModel


class Severity(str, Enum):
    NORMAL = "NORMAL"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class HealthResponse(BaseModel):
    status: Literal["ok"]
    service: str


class BaselineStats(BaseModel):
    ready: bool
    line_count_mean: Optional[float] = None
    line_count_std: Optional[float] = None
    error_rate_mean: Optional[float] = None
    error_rate_std: Optional[float] = None


class MetricsSnapshot(BaseModel):
    window_start: datetime
    window_end: datetime
    line_count: int
    error_count: int
    warn_count: int
    error_rate: float
    baseline: BaselineStats
    anomaly_score: float
    severity: Severity


class MetricsResponse(BaseModel):
    current: Optional[MetricsSnapshot] = None
    history: List[MetricsSnapshot] = []


class Alert(BaseModel):
    id: str
    created_at: datetime
    severity: Severity
    title: str
    description: str
    metric: str
    observed: float
    expected: float
    anomaly_score: float
    window_start: datetime
    window_end: datetime
    detector: str = "statistical"
    explanation: List[str] = []
    sample_lines: List[str] = []


class AlertsResponse(BaseModel):
    alerts: List[Alert]
    total: int
