import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from alembic import command
from alembic.config import Config
from fastapi.testclient import TestClient
from app.main import app
from app.database import get_db

TEST_DB_URL = "sqlite:///./test.db"


def setup_test_db():
    if os.path.exists("test.db"):
        os.remove("test.db")

    engine = create_engine(TEST_DB_URL, connect_args={
                           "check_same_thread": False})
    connection = engine.connect()
    transaction = connection.begin()

    alembic_cfg = Config("alembic.ini")
    alembic_cfg.set_main_option("sqlalchemy.url", TEST_DB_URL)
    command.upgrade(alembic_cfg, "head")

    SessionLocal = sessionmaker(bind=engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    return connection, transaction


def teardown_test_db(connection, transaction):
    transaction.rollback()
    connection.close()
