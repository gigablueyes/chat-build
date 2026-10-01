import { useState } from "react";
import type { GeneratedProject } from "../types";

interface ProjectListProps {
  projects: GeneratedProject[];
  onDelete: (id: string) => void;
}

export function ProjectList({ projects, onDelete }: ProjectListProps) {
  const [expanded, setExpanded] = useState<string | null>(null);

  if (projects.length === 0) {
    return <p className="empty-state">No projects generated yet. Create one above!</p>;
  }

  return (
    <ul className="project-list">
      {projects.map((project) => (
        <li key={project.id} className={`project-item status-${project.status}`}>
          <div className="project-item-header">
            <div>
              <strong>{project.name}</strong>
              <span className="badge">{project.language}</span>
              <span className="badge">{project.project_type}</span>
              <span className={`status status-${project.status}`}>{project.status}</span>
            </div>
            <div className="project-item-actions">
              <button
                type="button"
                onClick={() => setExpanded(expanded === project.id ? null : project.id)}
              >
                {expanded === project.id ? "Hide files" : "View files"}
              </button>
              <button type="button" className="danger" onClick={() => onDelete(project.id)}>
                Delete
              </button>
            </div>
          </div>
          <p>{project.description}</p>
          {project.error_message && <p className="error">{project.error_message}</p>}
          {expanded === project.id && (
            <div className="file-list">
              {Object.entries(project.files).map(([path, content]) => (
                <details key={path}>
                  <summary>{path}</summary>
                  <pre>{content}</pre>
                </details>
              ))}
            </div>
          )}
        </li>
      ))}
    </ul>
  );
}
