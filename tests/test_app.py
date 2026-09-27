import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app  # noqa: E402


@pytest.fixture
def client():
    """Create test client"""
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    """Test health endpoint"""
    response = client.get("/health")
    assert response.status_code == 200


def test_home(client):
    """Test home page"""
    response = client.get("/")
    assert response.status_code == 200


def test_create(client):
    """Test create page"""
    response = client.get("/create")
    assert response.status_code == 200


def test_api(client):
    """Test API endpoint"""
    response = client.get("/api/incidents")
    assert response.status_code == 200
