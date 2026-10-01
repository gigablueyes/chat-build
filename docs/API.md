# API Reference

Base URL: `http://localhost:8000/api/v1` (or your deployed backend URL).
Full interactive docs (Swagger UI) are always available at `/docs`, and the
OpenAPI schema at `/openapi.json`.

## Authentication

### `POST /auth/register`

Create a new user account.

```json
{
  "email": "user@example.com",
  "password": "at-least-8-characters",
  "full_name": "Optional Name"
}
```

### `POST /auth/login`

Exchange credentials for a JWT access token.

```json
{ "email": "user@example.com", "password": "at-least-8-characters" }
```

Response:

```json
{ "access_token": "<jwt>", "token_type": "bearer" }
```

Include the token in the `Authorization` request header prefixed with the word "Bearer" followed by a space and the access token value.

## Projects (code generation)

All endpoints below require the `Authorization` header.

### `POST /projects`

Submit a code generation request.

```json
{
  "name": "Todo API",
  "description": "A REST API for managing a todo list with user accounts",
  "language": "python",
  "project_type": "api"
}
```

- `language`: one of `python`, `javascript`, `typescript`, `java`, `csharp`, `php`, `go`
- `project_type`: one of `web_app`, `api`, `cli`, `other`

Returns the created `GeneratedProject`, including a `files` map of
`path -> file content` once generation completes (`status: "completed"`).

### `GET /projects`

List all projects owned by the current user.

### `GET /projects/{project_id}`

Fetch a single project.

### `DELETE /projects/{project_id}`

Delete a project. Returns `204 No Content`.

## Metadata

### `GET /health`

Simple health check, returns `{"status": "ok"}`.

### `GET /meta/languages`

Returns the supported `languages` and `project_types`, useful for populating
the frontend's selection dropdowns.
