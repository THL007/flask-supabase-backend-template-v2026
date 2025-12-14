"""API endpoint tests."""
import pytest
from app import create_app


@pytest.fixture
def client():
    """Create test client."""
    app = create_app("testing")
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test health check endpoint."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_web_health(client):
    """Test web health endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"

