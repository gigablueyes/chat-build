"""Application configuration using environment-based settings.

Supports multiple deployment stages (dev, staging, prod) via the
``ENVIRONMENT`` variable and a corresponding ``.env.<environment>`` file.
"""
from functools import lru_cache
from typing import List, Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Central application settings, loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=(".env", ".env.local"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # General
    PROJECT_NAME: str = "AI Code Generator"
    ENVIRONMENT: Literal["dev", "staging", "prod", "test"] = "dev"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Security
    SECRET_KEY: str = "change-this-secret-key-in-production"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24
    ALGORITHM: str = "HS256"

    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173"]

    # Database
    DATABASE_URL: str = "sqlite:///./chatbuild.db"

    # LLM provider
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"
    LLM_PROVIDER: Literal["openai", "mock"] = "mock"

    # Deployment
    GITHUB_PAGES_BASE_URL: str = ""
    CLOUD_PROVIDER: Literal["none", "aws", "gcp", "azure"] = "none"

    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT == "prod"


@lru_cache
def get_settings() -> Settings:
    """Return a cached Settings instance."""
    return Settings()


settings = get_settings()
