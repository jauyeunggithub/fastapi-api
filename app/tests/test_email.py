def test_send_email(client):
    r = client.post(
        "/send-email", json={"email": "test@example.com", "message": "Hello!"})
    assert r.status_code == 200
    assert r.json()["status"] == "sent"
