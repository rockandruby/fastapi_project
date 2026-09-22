import pytest
from fastapi.testclient import TestClient
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine
from sqlmodel import Session
from app.settings import DATABASE_TEST_URL

from app.api.deps import get_current_user, create_access_token
from app.models.user import User
from app.database import get_session
from app.main import app


test_engine = create_engine(DATABASE_TEST_URL)

@pytest.fixture(scope="session", autouse=True)
def setup_database():
    alembic_cfg = Config("alembic.ini")

    # Tell Alembic which database to migrate
    alembic_cfg.set_main_option(
        "sqlalchemy.url",
        DATABASE_TEST_URL,
    )

    command.upgrade(alembic_cfg, "head")

    yield

@pytest.fixture
def db_session():
    connection = test_engine.connect()
    transaction = connection.begin()

    session = Session(bind=connection)

    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()

@pytest.fixture
def client(db_session):
    def override_get_db():
        yield db_session

    app.dependency_overrides[get_session] = override_get_db

    with TestClient(app) as client:
        yield client

    app.dependency_overrides.clear()

@pytest.fixture(scope="module")
def skip_auth():
    def override_current_user():
        return User(
            id=1,
            name="Test Admin",
            email="admin@example.com",
        )

    app.dependency_overrides[get_current_user] = override_current_user

@pytest.fixture(scope="module")
def auth_header():
    def create_token(user_id):
        token = create_access_token(user_id)
        return {"Authorization": f"Bearer {token}"}
    return create_token
