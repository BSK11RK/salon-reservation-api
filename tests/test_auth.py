from fastapi.testclient import TestClient


def create_user(
    client: TestClient,
    email: str,
    password: str
):
    return client.post(
        "/users/",
        json={
            "name": "Test User",
            "email": email,
            "password": password
        }
    )


def test_login_success(client: TestClient):
    create_res = create_user(
        client,
        email="login@example.com",
        password="password123"
    )

    assert create_res.status_code == 201

    res = client.post(
        "/auth/login",
        data={
            "username": "login@example.com",
            "password": "password123"
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_with_wrong_password(client: TestClient):
    create_res = create_user(
        client,
        email="wrong-password@example.com",
        password="password123"
    )

    assert create_res.status_code == 201

    res = client.post(
        "/auth/login",
        data={
            "username": "wrong-password@example.com",
            "password": "wrongpassword"
        }
    )

    assert res.status_code == 401


def test_login_with_nonexistent_user(client: TestClient):
    res = client.post(
        "/auth/login",
        data={
            "username": "not-found@example.com",
            "password": "password123"
        }
    )

    assert res.status_code == 401