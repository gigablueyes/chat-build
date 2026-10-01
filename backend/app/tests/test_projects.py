"""Tests for the code generation project endpoints."""


def test_create_project_requires_auth(client):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "My App",
            "description": "A simple todo list web application",
            "language": "python",
            "project_type": "api",
        },
    )
    assert response.status_code == 401


def test_create_and_list_project(client, auth_headers):
    response = client.post(
        "/api/v1/projects",
        json={
            "name": "My App",
            "description": "A simple todo list web application",
            "language": "python",
            "project_type": "api",
        },
        headers=auth_headers,
    )
    assert response.status_code == 201
    body = response.json()
    assert body["status"] == "completed"
    assert "main.py" in body["files"]

    response = client.get("/api/v1/projects", headers=auth_headers)
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_project_not_found(client, auth_headers):
    response = client.get("/api/v1/projects/does-not-exist", headers=auth_headers)
    assert response.status_code == 404


def test_create_project_for_each_language(client, auth_headers):
    languages = ["python", "javascript", "typescript", "java", "csharp", "php", "go"]
    for language in languages:
        response = client.post(
            "/api/v1/projects",
            json={
                "name": f"App {language}",
                "description": "A simple inventory management API",
                "language": language,
                "project_type": "api",
            },
            headers=auth_headers,
        )
        assert response.status_code == 201, response.text
        assert response.json()["status"] == "completed"


def test_delete_project(client, auth_headers):
    create = client.post(
        "/api/v1/projects",
        json={
            "name": "Deletable",
            "description": "A project to be deleted shortly after creation",
            "language": "go",
            "project_type": "cli",
        },
        headers=auth_headers,
    )
    project_id = create.json()["id"]
    response = client.delete(f"/api/v1/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 204
    response = client.get(f"/api/v1/projects/{project_id}", headers=auth_headers)
    assert response.status_code == 404
