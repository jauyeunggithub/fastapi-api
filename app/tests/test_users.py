def test_register_and_login(client):
    r = client.post(
        "/register", json={"username": "alice", "password": "password"})
    assert r.status_code == 200
    assert "username" in r.json()
    assert r.json()["username"] == "alice"

    # Login the same user and ensure correct response
    r = client.post(
        "/login", json={"username": "alice", "password": "password"})
    assert r.status_code == 200
    assert "access_token" in r.json()


def test_register_duplicate_username(client):
    # Register the first user
    r = client.post(
        "/register", json={"username": "bob", "password": "password123"})
    assert r.status_code == 200

    # Attempt to register with the same username again
    r = client.post(
        "/register", json={"username": "bob", "password": "password123"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Username already registered"


def test_login_invalid_credentials(client):
    # Register a new user
    r = client.post(
        "/register", json={"username": "charlie", "password": "password123"})
    assert r.status_code == 200

    # Attempt login with incorrect password
    r = client.post(
        "/login", json={"username": "charlie", "password": "wrongpassword"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Invalid credentials"

    # Attempt login with non-existent user
    r = client.post(
        "/login", json={"username": "nonexistent", "password": "password123"})
    assert r.status_code == 400
    assert r.json()["detail"] == "Invalid credentials"


def test_register_empty_fields(client):
    # Attempt to register with empty fields
    r = client.post("/register", json={"username": "", "password": ""})
    assert r.status_code == 422  # Unprocessable Entity (validation error)


def test_login_empty_fields(client):
    # Attempt login with empty fields
    r = client.post("/login", json={"username": "", "password": ""})
    assert r.status_code == 422  # Unprocessable Entity (validation error)
