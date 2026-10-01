"""Tests for authentication endpoints."""


def test_register_and_login(client):
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "alice@example.com", "password": "strongpassword1"},
    )
    assert response.status_code == 201
    body = response.json()
    assert body["email"] == "alice@example.com"
    assert "id" in body

    response = client.post(
        "/api/v1/auth/login",
        json={"email": "alice@example.com", "password": "strongpassword1"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_register_duplicate_email(client):
    payload = {"email": "bob@example.com", "password": "strongpassword1"}
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    response = client.post("/api/v1/auth/register", json=payload)
    assert response.status_code == 400


def test_login_wrong_password(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "carol@example.com", "password": "strongpassword1"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "carol@example.com", "password": "wrongpassword"},
    )
    assert response.status_code == 401
