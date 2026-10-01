# Production Deployment Runbook

This is the exact, step-by-step checklist to take **chat-build** from "code
in the repository" to "running service". The repository already contains
everything needed (CI, deploy workflow, Docker image, Render blueprint); the
steps below are the remaining actions that must be performed by a repository
admin through the GitHub and Render web UIs (account creation, clicking
settings, and secret values cannot be done by an automated coding agent).

## 1. Enable GitHub Pages for the frontend

1. Go to the repository **Settings → Pages**.
2. Under "Build and deployment" → "Source", select **GitHub Actions**.
3. Nothing else to do here — `.github/workflows/deploy-pages.yml` already
   builds `frontend/` and publishes it on every push to `main`.
4. After the first successful run, the site URL appears at the top of the
   **Settings → Pages** page (typically
   `https://<owner>.github.io/<repo>/`).

## 2. Deploy the backend + PostgreSQL with the Render blueprint

The repository includes `render.yaml`, a [Render Blueprint](https://render.com/docs/blueprint-spec)
that provisions both the backend web service (built from
`backend/Dockerfile`) and a managed PostgreSQL database in one step.

1. Create a free account at https://render.com if you don't have one.
2. In the Render dashboard: **New → Blueprint**.
3. Connect this GitHub repository and select it. Render detects
   `render.yaml` automatically.
4. Click **Apply**. Render will:
   - Create the `chatbuild-db` PostgreSQL instance.
   - Build and deploy the `chatbuild-backend` web service from
     `backend/Dockerfile`.
   - Automatically wire `DATABASE_URL` to the new database and generate a
     random `SECRET_KEY`.
5. Once deployed, copy the backend's public URL, e.g.
   `https://chatbuild-backend.onrender.com`.

Any other provider works too (Railway, Fly.io, a VM, etc.) — see
`docs/CLOUD_MIGRATION.md` for the general pattern; only steps 2–5 above
would differ.

## 3. Apply database migrations

Render runs `backend/Dockerfile`'s `CMD` (`uvicorn`) but does not run
migrations automatically. After the first deploy, run them once:

- In the Render dashboard, open the `chatbuild-backend` service → **Shell**,
  and run:

  ```bash
  alembic upgrade head
  ```

- Alternatively, add a Render **Job** (or a one-off `render.yaml` job) that
  runs the same command before each deploy.

## 4. Configure the remaining backend environment variables

In the Render dashboard, under `chatbuild-backend` → **Environment**, set:

| Variable | Value |
| --- | --- |
| `BACKEND_CORS_ORIGINS` | `["https://<owner>.github.io"]` (the GitHub Pages origin from step 1) |
| `OPENAI_API_KEY` | (optional) your OpenAI key, only if enabling real LLM refinement |
| `LLM_PROVIDER` | `openai` (optional, only with the key above; defaults to `mock`) |

`SECRET_KEY` and `DATABASE_URL` are already set by the blueprint — do not
overwrite them with the placeholder values from `backend/.env.example`.

## 5. Point the frontend at the deployed backend

1. In the GitHub repository, go to **Settings → Secrets and variables →
   Actions → Variables**.
2. Add a repository variable named `VITE_API_BASE_URL` with the backend's
   public URL from step 2 (e.g. `https://chatbuild-backend.onrender.com`).
3. Re-run the `Deploy Frontend to GitHub Pages` workflow (Actions tab →
   select the workflow → **Run workflow**), or push any change under
   `frontend/` to trigger it automatically. The build step already reads
   `vars.VITE_API_BASE_URL` (see `.github/workflows/deploy-pages.yml`).

## 6. Verify everything works end to end

1. Open the GitHub Pages URL from step 1.
2. Register a new user, log in, and submit a code generation request.
3. Confirm the generated files appear in the dashboard.
4. If something fails, check the Render service logs
   (`chatbuild-backend` → **Logs**) for database connection or CORS errors.

---

**Summary of what you must do manually** (cannot be automated by a coding
agent): enable GitHub Pages in repository settings, create/connect a Render
account and apply the blueprint, run the one-off migration command, and set
the `BACKEND_CORS_ORIGINS` / `VITE_API_BASE_URL` values once real URLs exist.
Everything else (build, test, deploy automation, Docker image, migrations
themselves) is already implemented in the repository.
