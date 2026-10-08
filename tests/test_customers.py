from fastapi.testclient import TestClient

from app.models.user import User


def test_customer_can_get_own_profile(
    client: TestClient,
    customer_profile,
    customer_token: str,
    auth_headers
):
    res = client.get(
        "/customers/me",
        headers=auth_headers(customer_token)
    )

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == customer_profile.id
    assert data["user_id"] == customer_profile.user_id


def test_customer_cannot_create_customer(
    client: TestClient,
    customer_token: str,
    auth_headers,
    db_session
):
    target_user = User(
        name="Target Customer",
        email="target-customer@example.com",
        password_hash="not-used",
        role="customer"
    )

    db_session.add(target_user)
    db_session.commit()
    db_session.refresh(target_user)

    res = client.post(
        "/customers/",
        headers=auth_headers(customer_token),
        json={
            "user_id": target_user.id,
            "name": "Unauthorized Customer"
        }
    )

    assert res.status_code == 403


def test_admin_can_create_customer(
    client: TestClient,
    admin_token: str,
    auth_headers,
    db_session
):
    target_user = User(
        name="New Customer",
        email="new-customer@example.com",
        password_hash="not-used",
        role="customer"
    )

    db_session.add(target_user)
    db_session.commit()
    db_session.refresh(target_user)

    res = client.post(
        "/customers/",
        headers=auth_headers(admin_token),
        json={
            "user_id": target_user.id,
            "name": "New Customer"
        }
    )

    assert res.status_code == 201

    data = res.json()

    assert data["user_id"] == target_user.id
    assert data["name"] == "New Customer"


def test_admin_can_update_customer(
    client: TestClient,
    customer_profile,
    admin_token: str,
    auth_headers
):
    res = client.patch(
        f"/customers/{customer_profile.id}",
        headers=auth_headers(admin_token),
        json={"name": "Updated Customer"}
    )

    assert res.status_code == 200

    data = res.json()

    assert data["name"] == "Updated Customer"