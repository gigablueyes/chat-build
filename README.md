# chat-build — AI Code Generator

Generate production-ready project skeletons in multiple programming languages
from a natural language description, with automatic CI/CD and deployment.

## ✨ Features

- **AI-powered code generation** — describe an app in plain language and get a
  working project skeleton back (backend API, web app, CLI, etc.)
- **Multi-language support** — Python (FastAPI/Django), JavaScript/TypeScript
  (React/Node.js/Express), Java (Spring Boot), C# (.NET), PHP (Laravel), Go
- **Automatic deployment** — the frontend dashboard auto-deploys to GitHub
  Pages via GitHub Actions on every push to `main`; the architecture is ready
  to migrate to AWS/GCP/Azure later (see [`CLOUD_MIGRATION.md`](docs/CLOUD_MIGRATION.md))
- **Database management** — SQLAlchemy models with Alembic migrations,
  PostgreSQL in production (SQLite for local dev/tests), connection pooling
- **Authentication** — JWT-based auth so each user only sees their own
  generated projects

## 🏗️ Project structure

```
chat-build/
├── backend/            FastAPI backend (code generation API, auth, DB models)
│   ├── app/
│   │   ├── api/        REST endpoints (auth, projects, meta)
│   │   ├── core/       Settings & security (JWT, password hashing)
│   │   ├── db/         SQLAlchemy engine/session
│   │   ├── models/     ORM models (User, GeneratedProject)
│   │   ├── schemas/    Pydantic request/response schemas
│   │   ├── services/   Code generation orchestration (template + optional LLM)
│   │   ├── templates/  Per-language project skeleton generators
│   │   └── tests/      Pytest test suite
│   └── alembic/        Database migrations
├── frontend/           React + TypeScript dashboard (Vite)
├── docs/               Setup guide, API docs, cloud migration notes
├── docker-compose.yml  Local PostgreSQL + backend for development
└── .github/workflows/  CI (tests/build) and GitHub Pages deployment
```

## 🚀 Quick start

See [`docs/SETUP.md`](docs/SETUP.md) for full setup instructions. In short:

```bash
# Backend
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt -r requirements-dev.txt
cp .env.example .env
uvicorn app.main:app --reload

# Frontend (in another terminal)
cd frontend
npm install
cp .env.example .env
npm run dev
```

Open http://localhost:5173 to use the dashboard, and http://localhost:8000/docs
for the interactive API documentation.

## 📚 Documentation

- [Setup guide](docs/SETUP.md)
- [API reference](docs/API.md)
- [Production deployment runbook](docs/PRODUCTION_DEPLOYMENT.md)
- [Cloud migration guide](docs/CLOUD_MIGRATION.md)

## 🧪 Testing

```bash
cd backend && pytest app/tests
cd frontend && npm run lint && npm run build
```

## License

See [LICENSE](LICENSE).
