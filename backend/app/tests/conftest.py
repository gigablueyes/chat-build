"""Pytest fixtures: isolated in-memory SQLite DB per test session."""
import os

os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("LLM_PROVIDER", "mock")

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.session import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function", autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture()
def client():
    return TestClient(app)


@pytest.fixture()
def auth_headers(client):
    client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "supersecret123"},
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "test@example.com", "password": "supersecret123"},
    )
    token = response.json()["access_token"]
    return {"Authorization": "Bearer " + token}
