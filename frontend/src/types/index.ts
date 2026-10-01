export type ProjectLanguage =
  | "python"
  | "javascript"
  | "typescript"
  | "java"
  | "csharp"
  | "php"
  | "go";

export type ProjectType = "web_app" | "api" | "cli" | "other";

export type ProjectStatus =
  | "pending"
  | "generating"
  | "completed"
  | "failed"
  | "deployed";

export interface GeneratedProject {
  id: string;
  name: string;
  description: string;
  language: ProjectLanguage;
  project_type: ProjectType;
  status: ProjectStatus;
  files: Record<string, string>;
  deployment_url: string | null;
  error_message: string | null;
  owner_id: string;
  created_at: string;
  updated_at: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
}
