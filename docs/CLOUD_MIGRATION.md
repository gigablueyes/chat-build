# Cloud Migration Guide

The project is designed to start on GitHub Pages (frontend) + a single host
(backend/database) and migrate to a cloud provider once traffic/scale demands
it, without rewriting application code.

## What's already cloud-ready

- **Configuration is environment-driven** (`backend/app/core/config.py`):
  `DATABASE_URL`, `SECRET_KEY`, CORS origins, and the `CLOUD_PROVIDER` flag are
  all read from environment variables, so no code changes are needed to point
  at managed services.
- **PostgreSQL from day one** — the schema and Alembic migrations already
  target PostgreSQL, so moving from a self-hosted Postgres instance to a
  managed one (RDS, Cloud SQL, Azure Database for PostgreSQL) is just a
  connection-string change.
- **Stateless backend** — the FastAPI app holds no in-memory state, so it can
  run behind a load balancer or in a container orchestrator (ECS, Cloud Run,
  Azure Container Apps, Kubernetes) with multiple replicas.
- **Containerized** — `backend/Dockerfile` builds a deployable image usable by
  any container platform.

## Migration steps (example: AWS)

1. Provision an **RDS PostgreSQL** instance and set `DATABASE_URL` accordingly.
2. Push `backend/Dockerfile` to **ECR** and deploy via **ECS Fargate** or
   **App Runner**.
3. Run `alembic upgrade head` as a one-off task against the new database.
4. Point the frontend's `VITE_API_BASE_URL` at the new backend URL and
   redeploy (GitHub Pages, S3+CloudFront, or Amplify Hosting).
5. Set `CLOUD_PROVIDER=aws` in the backend environment for any
   provider-specific behavior you add later (e.g. S3 storage for generated
   project archives).

The same pattern applies to **Google Cloud** (Cloud SQL + Cloud Run) and
**Azure** (Azure Database for PostgreSQL + Container Apps) — only the managed
service names change, not the application code.
