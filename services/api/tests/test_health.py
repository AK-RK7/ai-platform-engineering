from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {
        "status": "healthy",
        "service": "ai-platform-api",
    }


def test_health_live():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json() == {
        "status": "alive",
    }


def test_health_ready():
    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
    }
