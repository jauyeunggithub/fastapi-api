import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base, get_db
from app.main import app
import subprocess
from fastapi.testclient import TestClient

# Use SQLite file-based DB for tests instead of in-memory SQLite
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create the engine with the updated DB URL
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a session maker for the testing database
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

# Override the get_db dependency to use the test session


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

# Fixture to apply migrations and create/drop tables before/after tests


@pytest.fixture(scope="function")
def db_session():
    # Apply the migration to the test database before each test
    subprocess.run(["alembic", "upgrade", "head"])  # Run Alembic migrations
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()
        # Drop tables after each test to reset the DB
        # Revert to the initial state
        subprocess.run(["alembic", "downgrade", "base"])

# Fixture for the TestClient that uses the overridden get_db


@pytest.fixture(scope="function")
def client(db_session):
    # Override the dependency to use the testing DB session
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
