"""GET /health: liveness probe."""

from fastapi import APIRouter

from app.config import SERVICE_NAME
from app.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok", service=SERVICE_NAME)
