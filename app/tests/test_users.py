def test_register_and_login(client):
    r = client.post("/register", json={"username": "alice", "password": "pwd"})
    assert r.status_code == 200

    r = client.post("/login", json={"username": "alice", "password": "pwd"})
    assert r.status_code == 200
    assert "access_token" in r.json()
