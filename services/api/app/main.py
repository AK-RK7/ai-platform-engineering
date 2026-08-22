import logging

from fastapi import FastAPI

from app.logging_config import configure_logging
from app.telemetry import configure_telemetry


configure_logging()

logger = logging.getLogger(__name__)

app = FastAPI()

configure_telemetry(app)


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