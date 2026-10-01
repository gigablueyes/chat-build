# Setup Guide

This guide walks through running **chat-build** locally for development.

## Prerequisites

- Python 3.12+
- Node.js 20+
- (Optional) Docker, for running PostgreSQL locally instead of SQLite

## 1. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
```

By default the backend uses SQLite (`DATABASE_URL=sqlite:///./chatbuild.db`)
so you can get started without any external services. To use PostgreSQL
instead:

```bash
docker compose up -d db
```

Then set in `backend/.env`:

```
DATABASE_URL=postgresql://<db_user>:<db_password>@localhost:5432/chatbuild
```

### Run database migrations

```bash
alembic upgrade head
```

### Start the API server

```bash
uvicorn app.main:app --reload
```

The API is now available at http://localhost:8000, with interactive docs at
http://localhost:8000/docs.

### Run tests

```bash
pytest app/tests --cov=app
```

## 2. Frontend

```bash
cd frontend
npm install
cp .env.example .env
npm run dev
```

The dashboard is now available at http://localhost:5173. Configure
`VITE_API_BASE_URL` in `frontend/.env` if your backend runs on a different
host/port.

### Lint & build

```bash
npm run lint
npm run build
```

## 3. Environment configuration (dev / staging / prod)

The backend reads configuration from environment variables (see
`backend/app/core/config.py`). Set `ENVIRONMENT=dev|staging|prod|test` plus
the relevant `DATABASE_URL`, `SECRET_KEY`, and `BACKEND_CORS_ORIGINS` for each
stage. Never reuse the default `SECRET_KEY` outside local development.

## 4. Enabling real AI-powered generation

By default `LLM_PROVIDER=mock`, so code is generated entirely from the
built-in templates with no external calls. To enable OpenAI-based refinement
of the generated README/overview, set:

```
LLM_PROVIDER=openai
OPENAI_API_KEY=sk-...
```

## 5. Deployment

Pushing to `main` triggers `.github/workflows/deploy-pages.yml`, which builds
the frontend and publishes it to GitHub Pages. Enable GitHub Pages for the
repository (Settings → Pages → Source: GitHub Actions) to activate this.

See [`CLOUD_MIGRATION.md`](CLOUD_MIGRATION.md) for moving the backend/database
to a cloud provider later.
