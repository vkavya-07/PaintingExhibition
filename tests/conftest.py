import pytest
from sqlmodel import SQLModel, create_engine, Session
from app.main import app
from fastapi.testclient import TestClient
from app.db import get_session

import os

TEST_DB = os.path.join(os.path.dirname(__file__), "test.db")
if os.path.exists(TEST_DB):
    os.remove(TEST_DB)
DATABASE_URL = f"sqlite:///{TEST_DB}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

@pytest.fixture(name="session")
def session_fixture():
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    client = TestClient(app)
    # override dependency
    def get_session_override():
        with Session(engine) as s:
            yield s
    app.dependency_overrides[get_session] = get_session_override
    try:
        yield client
    finally:
        app.dependency_overrides.clear()