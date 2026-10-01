"""Health-check and metadata endpoint."""
from fastapi import APIRouter

from app.models.project import ProjectLanguage, ProjectType

router = APIRouter(tags=["meta"])


@router.get("/health")
def health_check():
    return {"status": "ok"}


@router.get("/meta/languages")
def supported_languages():
    return {
        "languages": [lang.value for lang in ProjectLanguage],
        "project_types": [pt.value for pt in ProjectType],
    }
