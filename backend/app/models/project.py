"""ORM models for generated code projects."""
import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, JSON, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.session import Base


class ProjectLanguage(str, enum.Enum):
    PYTHON = "python"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    JAVA = "java"
    CSHARP = "csharp"
    PHP = "php"
    GO = "go"


class ProjectType(str, enum.Enum):
    WEB_APP = "web_app"
    API = "api"
    CLI = "cli"
    OTHER = "other"


class ProjectStatus(str, enum.Enum):
    PENDING = "pending"
    GENERATING = "generating"
    COMPLETED = "completed"
    FAILED = "failed"
    DEPLOYED = "deployed"


class GeneratedProject(Base):
    __tablename__ = "generated_projects"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    language: Mapped[ProjectLanguage] = mapped_column(Enum(ProjectLanguage), nullable=False)
    project_type: Mapped[ProjectType] = mapped_column(Enum(ProjectType), nullable=False)
    status: Mapped[ProjectStatus] = mapped_column(
        Enum(ProjectStatus), default=ProjectStatus.PENDING, nullable=False
    )
    files: Mapped[dict] = mapped_column(JSON, default=dict)
    deployment_url: Mapped[str] = mapped_column(String(500), nullable=True)
    error_message: Mapped[str] = mapped_column(Text, nullable=True)

    owner_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"), nullable=False)
    owner = relationship("User", back_populates="projects")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
