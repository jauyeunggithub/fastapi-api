from fastapi.testclient import TestClient
from app.tests.shared import setup_test_db, teardown_test_db
from app.main import app


def test_create_book():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post(
            "/register", json={"username": "bob", "password": "password"})
        assert r.status_code == 200

        r = client.post(
            "/login", json={"username": "bob", "password": "password"})
        assert r.status_code == 200
        token = r.json().get("access_token")
        assert token is not None

        headers = {"Authorization": f"Bearer {token}"}
        r = client.post("/books", json={"title": "1984"}, headers=headers)
        assert r.status_code == 200
        assert r.json()["title"] == "1984"

    teardown_test_db(connection, transaction)


def test_create_book_unauthorized():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post("/books", json={"title": "Animal Farm"})
        assert r.status_code == 401

    teardown_test_db(connection, transaction)


def test_create_book_invalid_token():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        invalid_headers = {"Authorization": "Bearer invalid_token"}
        r = client.post(
            "/books", json={"title": "Brave New World"}, headers=invalid_headers)
        assert r.status_code == 401

    teardown_test_db(connection, transaction)


def test_create_book_invalid_data():
    connection, transaction = setup_test_db()
    with TestClient(app) as client:
        r = client.post(
            "/register", json={"username": "bob", "password": "password"})
        assert r.status_code == 200

        r = client.post(
            "/login", json={"username": "bob", "password": "password"})
        assert r.status_code == 200
        token = r.json().get("access_token")
        assert token is not None

        headers = {"Authorization": f"Bearer {token}"}
        r = client.post("/books", json={"title": ""}, headers=headers)
        assert r.status_code == 422
        assert "detail" in r.json()

    teardown_test_db(connection, transaction)
