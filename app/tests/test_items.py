def test_create_book(client):
    client.post("/register", json={"username": "bob", "password": "pwd"})
    r = client.post("/login", json={"username": "bob", "password": "pwd"})
    token = r.json()["access_token"]

    headers = {"Authorization": f"Bearer {token}"}
    r = client.post("/books", json={"title": "1984"}, headers=headers)
    assert r.status_code == 200
    assert r.json()["title"] == "1984"
