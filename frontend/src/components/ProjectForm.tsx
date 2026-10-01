import { useState } from "react";
import type { ProjectLanguage, ProjectType } from "../types";

interface ProjectFormProps {
  languages: ProjectLanguage[];
  projectTypes: ProjectType[];
  onSubmit: (values: {
    name: string;
    description: string;
    language: ProjectLanguage;
    project_type: ProjectType;
  }) => Promise<void>;
  submitting: boolean;
}

export function ProjectForm({ languages, projectTypes, onSubmit, submitting }: ProjectFormProps) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [language, setLanguage] = useState<ProjectLanguage>(languages[0] ?? "python");
  const [projectType, setProjectType] = useState<ProjectType>(projectTypes[0] ?? "web_app");

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    await onSubmit({ name, description, language, project_type: projectType });
    setName("");
    setDescription("");
  }

  return (
    <form className="project-form" onSubmit={handleSubmit}>
      <h2>Generate a new project</h2>
      <label>
        Project name
        <input value={name} onChange={(e) => setName(e.target.value)} required />
      </label>
      <label>
        Describe what you want to build
        <textarea
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          required
          minLength={10}
          rows={4}
          placeholder="e.g. A REST API for managing a todo list with user accounts"
        />
      </label>
      <div className="form-row">
        <label>
          Language
          <select value={language} onChange={(e) => setLanguage(e.target.value as ProjectLanguage)}>
            {languages.map((lang) => (
              <option key={lang} value={lang}>
                {lang}
              </option>
            ))}
          </select>
        </label>
        <label>
          Project type
          <select
            value={projectType}
            onChange={(e) => setProjectType(e.target.value as ProjectType)}
          >
            {projectTypes.map((type) => (
              <option key={type} value={type}>
                {type}
              </option>
            ))}
          </select>
        </label>
      </div>
      <button type="submit" disabled={submitting}>
        {submitting ? "Generating…" : "Generate code"}
      </button>
    </form>
  );
}
