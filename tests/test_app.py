import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200

def test_home(client):
    r = client.get("/")
    assert r.status_code == 200

def test_create(client):
    r = client.get("/create")
    assert r.status_code == 200

def test_api(client):
    r = client.get("/api/incidents")
    assert r.status_code == 200