from app import app


def test_homepage():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_create_page():
    client = app.test_client()
    response = client.get("/create")
    assert response.status_code == 200