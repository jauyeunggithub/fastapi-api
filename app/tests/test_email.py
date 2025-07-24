import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

# Path to the test database file
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


# Example test using file-based SQLite DB and transactions
def test_send_email():
    # Set up the database for the test
    connection, transaction = setup_test_db()

    with TestClient(app) as client:
        # Sending an email request
        r = client.post(
            "/send-email", json={"email": "test@example.com", "message": "Hello!"})

        # Assertions to verify that the email was sent successfully
        assert r.status_code == 200
        assert r.json()["status"] == "sent"

    # Rollback the transaction to ensure no changes are persisted
    transaction.rollback()

    # Close the connection
    connection.close()
