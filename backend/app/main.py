"""FastAPI entrypoint.

Run from the `backend/` directory:

    uvicorn app.main:app --reload
"""

from fastapi import FastAPI

from app import __version__
from app.api import health
from app.config import SERVICE_NAME


def create_app() -> FastAPI:
    app = FastAPI(title=SERVICE_NAME, version=__version__)

    app.include_router(health.router)
    # Planned (see docs/api-contract.md):
    #   app.include_router(metrics.router)     GET /metrics
    #   app.include_router(alerts.router)      GET /alerts
    #   app.include_router(websockets.router)  WS  /ws/metrics, /ws/alerts

    return app


app = create_app()
