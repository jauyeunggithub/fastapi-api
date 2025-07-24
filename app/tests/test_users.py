from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from alembic import command
from alembic.config import Config
import os

from app.main import app
from app.database import get_db

TEST_DB_URL = "sqlite:///./test.db"


def setup_test_db():
    # Remove existing test.db before each test to start fresh
    if os.path.exists("test.db"):
        os.remove("test.db")

    # Create a new SQLite engine pointing to the test file
    engine = create_engine(TEST_DB_URL, connect_args={
                           "check_same_thread": False})

    # Create a connection to the engine
    connection = engine.connect()

    # Start a new transaction
    transaction = connection.begin()

    # Run Alembic migrations on the test database
    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

    # Create a session maker bound to the test engine
    SessionLocal = sessionmaker(bind=engine)

    # Override the get_db dependency to use this session
    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Apply the override
    app.dependency_overrides[get_db] = override_get_db

    return connection, transaction


def test_register_and_login():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post(
            "/register", json={"username": "alice", "password": "password"})
        assert r.status_code == 200
        assert "username" in r.json()
        assert r.json()["username"] == "alice"

        r = client.post(
            "/login", json={"username": "alice", "password": "password"})
        assert r.status_code == 200
        assert "access_token" in r.json()

    transaction.rollback()
    connection.close()


def test_register_duplicate_username():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post(
            "/register", json={"username": "bob", "password": "password123"})
        assert r.status_code == 200

        r = client.post(
            "/register", json={"username": "bob", "password": "password123"})
        assert r.status_code == 400
        assert r.json()["detail"] == "Username already registered"

    transaction.rollback()
    connection.close()


def test_login_invalid_credentials():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post(
            "/register", json={"username": "charlie", "password": "password123"})
        assert r.status_code == 200

        r = client.post(
            "/login", json={"username": "charlie", "password": "wrongpassword"})
        assert r.status_code == 400
        assert r.json()["detail"] == "Invalid credentials"

        r = client.post(
            "/login", json={"username": "nonexistent", "password": "password123"})
        assert r.status_code == 400
        assert r.json()["detail"] == "Invalid credentials"

    transaction.rollback()
    connection.close()


def test_register_empty_fields():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post("/register", json={"username": "", "password": ""})
        assert r.status_code == 422

    transaction.rollback()
    connection.close()


def test_login_empty_fields():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post("/login", json={"username": "", "password": ""})
        assert r.status_code == 422

    transaction.rollback()
    connection.close()
