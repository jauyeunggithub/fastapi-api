def test_create_book(client):
    r = client.post(
        "/register", json={"username": "bob", "password": "password"})
    assert r.status_code == 200

    r = client.post("/login", json={"username": "bob", "password": "password"})
    assert r.status_code == 200
    token = r.json().get("access_token")
    assert token is not None

    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/books", json={"title": "1984"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["title"] == "1984"
