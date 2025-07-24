from fastapi.testclient import TestClient
from app.tests.shared import setup_test_db, teardown_test_db
from app.main import app


def test_send_email():
    connection, transaction = setup_test_db()

    with TestClient(app) as client:
        r = client.post(
            "/send-email", json={"email": "test@example.com", "message": "Hello!"})

        assert r.status_code == 200
        assert r.json()["status"] == "sent"

    teardown_test_db(connection, transaction)
