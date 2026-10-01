import { useEffect, useState } from "react";
import "./App.css";
import { api, ApiError } from "./api/client";
import { AuthPanel } from "./components/AuthPanel";
import { ProjectForm } from "./components/ProjectForm";
import { ProjectList } from "./components/ProjectList";
import type { GeneratedProject, ProjectLanguage, ProjectType } from "./types";

const TOKEN_STORAGE_KEY = "chatbuild_token";

function App() {
  const [token, setToken] = useState<string | null>(() =>
    localStorage.getItem(TOKEN_STORAGE_KEY),
  );
  const [projects, setProjects] = useState<GeneratedProject[]>([]);
  const [languages, setLanguages] = useState<ProjectLanguage[]>([]);
  const [projectTypes, setProjectTypes] = useState<ProjectType[]>([]);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    api
      .supportedLanguages()
      .then(({ languages, project_types }) => {
        setLanguages(languages);
        setProjectTypes(project_types);
      })
      .catch(() => {
        // Backend may be unavailable; the form will fall back to empty selects.
      });
  }, []);

  useEffect(() => {
    if (!token) return;
    api
      .listProjects(token)
      .then(setProjects)
      .catch((err) => setError(err instanceof ApiError ? err.message : "Failed to load projects"));
  }, [token]);

  function handleAuthenticated(newToken: string) {
    localStorage.setItem(TOKEN_STORAGE_KEY, newToken);
    setToken(newToken);
  }

  function handleLogout() {
    localStorage.removeItem(TOKEN_STORAGE_KEY);
    setToken(null);
    setProjects([]);
  }

  async function handleCreateProject(values: {
    name: string;
    description: string;
    language: ProjectLanguage;
    project_type: ProjectType;
  }) {
    if (!token) return;
    setSubmitting(true);
    setError(null);
    try {
      const project = await api.createProject(token, values);
      setProjects((prev) => [project, ...prev]);
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to generate project");
    } finally {
      setSubmitting(false);
    }
  }

  async function handleDeleteProject(id: string) {
    if (!token) return;
    try {
      await api.deleteProject(token, id);
      setProjects((prev) => prev.filter((p) => p.id !== id));
    } catch (err) {
      setError(err instanceof ApiError ? err.message : "Failed to delete project");
    }
  }

  return (
    <div className="app">
      <header>
        <h1>AI Code Generator</h1>
        <p>Describe an application in plain language and generate a ready-to-use project skeleton.</p>
        {token && (
          <button type="button" onClick={handleLogout}>
            Sign out
          </button>
        )}
      </header>

      {error && <p className="error">{error}</p>}

      {!token ? (
        <AuthPanel onAuthenticated={handleAuthenticated} />
      ) : (
        <main>
          <ProjectForm
            languages={languages}
            projectTypes={projectTypes}
            onSubmit={handleCreateProject}
            submitting={submitting}
          />
          <ProjectList projects={projects} onDelete={handleDeleteProject} />
        </main>
      )}
    </div>
  );
}

export default App;
