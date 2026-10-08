from fastapi.testclient import TestClient


def create_user(
    client: TestClient,
    name: str,
    email: str,
    password: str
):
    return client.post(
        "/users/",
        json={
            "name": name,
            "email": email,
            "password": password
        }
    )
    
    
def login(
    client: TestClient,
    email: str,
    password: str
):
    return client.post(
        "/auth/login",
        data={
            "username": email,
            "password": password
        }
    )


def test_create_user(client: TestClient):
    res = create_user(
        client,
        name="Test User",
        email="test@example.com",
        password="password123"
    )

    assert res.status_code == 201

    data = res.json()

    assert data["name"] == "Test User"
    assert data["email"] == "test@example.com"
    assert data["role"] == "customer"
    
    
def test_create_user_with_invalid_email(client: TestClient):
    res = create_user(
        client,
        name="Test User",
        email="invalid-email",
        password="password123"
    )
    
    assert res.status_code == 422
    
    
def test_create_user_with_short_password(client: TestClient):
    res = create_user(
        client,
        name="Test User",
        email="short@example.com",
        password="1234567"
    )

    assert res.status_code == 422


def test_create_user_with_duplicate_email(client: TestClient):
    first_res = create_user(
        client,
        name="First User",
        email="duplicate@example.com",
        password="password123"
    )

    assert first_res.status_code == 201

    second_res = create_user(
        client,
        name="Second User",
        email="duplicate@example.com",
        password="password123"
    )

    assert second_res.status_code == 409


def test_get_current_user(client: TestClient):
    create_res = create_user(
        client,
        name="Test User",
        email="me@example.com",
        password="password123"
    )

    assert create_res.status_code == 201

    login_res = login(
        client,
        email="me@example.com",
        password="password123"
    )

    assert login_res.status_code == 200

    token = login_res.json()["access_token"]

    res = client.get(
        "/users/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert res.status_code == 200

    data = res.json()

    assert data["email"] == "me@example.com"
    assert data["role"] == "customer"