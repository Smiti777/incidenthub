import pytest
import sys
import os

# Add parent directory to path so we can import app
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app


@pytest.fixture
def client():
    """Create test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health_endpoint(client):
    """Test that /health endpoint returns status ok"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "ok"
    assert "commit" in data


def test_home_page(client):
    """Test that home page loads successfully"""
    response = client.get("/")
    assert response.status_code == 200


def test_create_incident_form(client):
    """Test that create incident form page loads"""
    response = client.get("/create")
    assert response.status_code == 200


def test_api_incidents(client):
    """Test that /api/incidents returns JSON with incidents array"""
    response = client.get("/api/incidents")
    assert response.status_code == 200
    data = response.get_json()
    assert "incidents" in data
    assert isinstance(data["incidents"], list)