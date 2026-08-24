import logging

from fastapi import FastAPI

from app.logging_config import configure_logging
from app.telemetry import configure_telemetry

from prometheus_client import make_asgi_app
from app.middleware import MetricsMiddleware

from app.routers.models import router as models_router
from app.routers.inference import router as inference_router

configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

configure_telemetry(app)

app.add_middleware(MetricsMiddleware)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

app.include_router(models_router)
app.include_router(inference_router)

@app.get("/health")
def health():
    logger.info("health_check")

    return {
        "status": "healthy",
        "service": "ai-platform-api",
    }


@app.get("/health/live")
def liveness():
    logger.info("liveness_check")

    return {
        "status": "alive",
    }


@app.get("/health/ready")
def readiness():
    logger.info("readiness_check")

    return {
        "status": "ready",
    }