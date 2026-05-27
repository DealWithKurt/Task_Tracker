from fastapi.testclient import TestClient

def test_register_user(client: TestClient):
    response = client.post(
        "/auth/register",
        json={
            "name": "New User",
            "email": "newuser123@example.com",
            "password": "password123",
            "role": "user"
        }
    )
    assert response.status_code == 200
    assert response.json()["email"] == "newuser123@example.com"
    assert "password" not in response.json()

def test_login_user(client: TestClient, test_user):
    response = client.post(
        "/auth/login",
        data={"username": "test@example.com", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"

def test_unauthorized_access(client: TestClient):
    response = client.get("/auth/me")
    assert response.status_code == 401
