"""Project (code generation request) schemas."""
from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.project import ProjectLanguage, ProjectStatus, ProjectType


class ProjectCreate(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=10, description="Natural language description of the app to generate")
    language: ProjectLanguage
    project_type: ProjectType = ProjectType.WEB_APP


class ProjectUpdate(BaseModel):
    status: ProjectStatus | None = None
    deployment_url: str | None = None
    error_message: str | None = None


class ProjectOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    name: str
    description: str
    language: ProjectLanguage
    project_type: ProjectType
    status: ProjectStatus
    files: dict[str, str] = {}
    deployment_url: str | None = None
    error_message: str | None = None
    owner_id: str
    created_at: datetime
    updated_at: datetime
