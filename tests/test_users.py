from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_and_read_users():
    # create admin
    res = client.post("/users", json={
        "username": "admin01",
        "email": "admin@example.com",
        "password": "Admin123!",
        "role": "admin"
    })
    assert res.status_code == 201
    admin = res.json()

    headers = {"X-User-Id": admin["id"], "X-User-Role": "admin"}
    # admin can get all
    res2 = client.get("/users", headers=headers)
    assert res2.status_code == 200
    assert any(u["username"] == "admin01" for u in res2.json())
