"""API v1 router aggregation."""
from fastapi import APIRouter

from app.api import auth, meta, projects

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(projects.router)
api_router.include_router(meta.router)
