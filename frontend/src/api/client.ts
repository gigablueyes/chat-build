import type { AuthResponse, GeneratedProject, ProjectLanguage, ProjectType } from "../types";

const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string | undefined) || "http://localhost:8000";

const API_PREFIX = "/api/v1";

class ApiError extends Error {
  status: number;
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
  }
}

async function request<T>(
  path: string,
  options: RequestInit = {},
  token?: string | null,
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> | undefined),
  };
  if (token) {
    headers.Authorization = "Bearer " + token;
  }

  const response = await fetch(`${API_BASE_URL}${API_PREFIX}${path}`, {
    ...options,
    headers,
  });

  if (!response.ok) {
    let detail = response.statusText;
    try {
      const body = await response.json();
      detail = body.detail ?? detail;
    } catch {
      // ignore JSON parse errors on error responses
    }
    throw new ApiError(detail, response.status);
  }

  if (response.status === 204) {
    return undefined as T;
  }

  return (await response.json()) as T;
}

export const api = {
  register: (email: string, password: string, full_name?: string) =>
    request("/auth/register", {
      method: "POST",
      body: JSON.stringify({ email, password, full_name }),
    }),

  login: (email: string, password: string) =>
    request<AuthResponse>("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),

  listProjects: (token: string) =>
    request<GeneratedProject[]>("/projects", { method: "GET" }, token),

  createProject: (
    token: string,
    payload: { name: string; description: string; language: ProjectLanguage; project_type: ProjectType },
  ) =>
    request<GeneratedProject>(
      "/projects",
      { method: "POST", body: JSON.stringify(payload) },
      token,
    ),

  deleteProject: (token: string, id: string) =>
    request<void>(`/projects/${id}`, { method: "DELETE" }, token),

  supportedLanguages: () =>
    request<{ languages: ProjectLanguage[]; project_types: ProjectType[] }>(
      "/meta/languages",
      { method: "GET" },
    ),
};

export { ApiError };
