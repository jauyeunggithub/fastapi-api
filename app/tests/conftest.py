import os
import pytest
import logging
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db  # Assuming get_db is in app.database
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# Configure logging to print to stdout
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Function to log database connections


def get_db():
    db_url = os.getenv("DATABASE_URL", "sqlite:///:memory:")
    engine = create_engine(db_url, connect_args={"check_same_thread": False})
    logger.info(f"Connecting to database: {db_url}")
    return engine.connect()

# Fixture to create a temporary SQLite database for each test


@pytest.fixture(scope="function")
def db_session():
    db_file = "./test.db"

    if os.path.exists(db_file):
        os.remove(db_file)

    SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_file}"
    engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                           "check_same_thread": False})

    # Create the session maker for the testing database
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=engine)

    # Create all tables (no migrations, just raw table creation)
    Base.metadata.create_all(bind=engine)

    # Override the get_db dependency to use the test session
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    # Start a session
    session = TestingSessionLocal()

    # Function to clear all rows in all tables
    def clear_all_tables():
        for table in reversed(Base.metadata.sorted_tables):
            try:
                # Instead of `session.execute(table.delete())`, we use a transaction and rollback
                session.execute(table.delete())
            except OperationalError:
                pass  # Ignore any errors due to foreign key constraints
        session.commit()

    # Ensure tables are created and clear all data before the test starts
    try:
        logger.info("Clearing database tables before the test...")
        clear_all_tables()
        yield session
    finally:
        # Cleanup: Close session and optionally remove the SQLite DB file after each test
        session.close()
        # Optionally, delete the database file only if tests pass
        if os.path.exists(db_file):
            os.remove(db_file)

# Fixture for the TestClient that uses the overridden get_db


@pytest.fixture(scope="function")
def client(db_session):
    # Ensure the dependency is overridden before FastAPI is initialized
    app.dependency_overrides[get_db] = lambda: db_session
    with TestClient(app) as c:
        yield c
