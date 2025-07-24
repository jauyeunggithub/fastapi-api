def test_register_and_login(client):
    # Register user with correct schema
    r = client.post(
        "/register", json={"username": "alice", "password": "password"})
    assert r.status_code == 200

    # Login the same user and ensure correct response
    r = client.post(
        "/login", json={"username": "alice", "password": "password"})
    assert r.status_code == 200
    assert "access_token" in r.json()
