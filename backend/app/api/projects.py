"""Endpoints for submitting and managing code generation requests."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.project import GeneratedProject, ProjectStatus
from app.models.user import User
from app.schemas.project import ProjectCreate, ProjectOut
from app.services.code_generation import code_generation_service

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectOut, status_code=status.HTTP_201_CREATED)
def create_project(
    project_in: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = GeneratedProject(
        name=project_in.name,
        description=project_in.description,
        language=project_in.language,
        project_type=project_in.project_type,
        status=ProjectStatus.GENERATING,
        owner_id=current_user.id,
    )
    db.add(project)
    db.commit()
    db.refresh(project)

    try:
        files = code_generation_service.generate_project(
            name=project.name,
            description=project.description,
            language=project.language,
            project_type=project.project_type,
        )
        project.files = files
        project.status = ProjectStatus.COMPLETED
    except Exception as exc:  # pragma: no cover - defensive guard
        project.status = ProjectStatus.FAILED
        project.error_message = str(exc)

    db.commit()
    db.refresh(project)
    return project


@router.get("", response_model=list[ProjectOut])
def list_projects(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return db.query(GeneratedProject).filter(GeneratedProject.owner_id == current_user.id).all()


@router.get("/{project_id}", response_model=ProjectOut)
def get_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(GeneratedProject)
        .filter(GeneratedProject.id == project_id, GeneratedProject.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    return project


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(
    project_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    project = (
        db.query(GeneratedProject)
        .filter(GeneratedProject.id == project_id, GeneratedProject.owner_id == current_user.id)
        .first()
    )
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")
    db.delete(project)
    db.commit()
