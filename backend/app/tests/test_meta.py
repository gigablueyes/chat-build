"""Tests for health and metadata endpoints."""


def test_health_check(client):
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["name"]


def test_supported_languages(client):
    response = client.get("/api/v1/meta/languages")
    assert response.status_code == 200
    body = response.json()
    assert "python" in body["languages"]
    assert "web_app" in body["project_types"]
