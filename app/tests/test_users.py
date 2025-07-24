from fastapi.testclient import TestClient
from app.tests.shared import setup_test_db, teardown_test_db
from app.main import app


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

    teardown_test_db(connection, transaction)


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

    teardown_test_db(connection, transaction)


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

    teardown_test_db(connection, transaction)


def test_register_empty_fields():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post("/register", json={"username": "", "password": ""})
        assert r.status_code == 422

    teardown_test_db(connection, transaction)


def test_login_empty_fields():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post("/login", json={"username": "", "password": ""})
        assert r.status_code == 422

    teardown_test_db(connection, transaction)
