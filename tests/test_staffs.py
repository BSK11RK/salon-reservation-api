from fastapi.testclient import TestClient

from app.models.user import User


def test_staff_can_get_own_profile(
    client: TestClient,
    staff_user,
    staff_token: str,
    auth_headers
):
    res = client.get(
        "/staffs/me",
        headers=auth_headers(staff_token)
    )

    assert res.status_code == 200

    data = res.json()

    assert data["user_id"] == staff_user.id


def test_admin_can_create_staff(
    client: TestClient,
    db_session,
    salon,
    admin_token: str,
    auth_headers
):
    target_user = User(
        name="New Staff",
        email="new-staff@example.com",
        password_hash="not-used-in-this-test",
        role="customer"
    )

    db_session.add(target_user)
    db_session.commit()
    db_session.refresh(target_user)

    res = client.post(
        "/staffs/",
        headers=auth_headers(admin_token),
        json={
            "user_id": target_user.id,
            "name": "New Staff",
            "salon_id": salon.id
        }
    )

    assert res.status_code == 201

    data = res.json()

    assert data["user_id"] == target_user.id
    assert data["salon_id"] == salon.id

    db_session.refresh(target_user)

    assert target_user.role == "staff"


def test_customer_cannot_create_staff(
    client: TestClient,
    customer_token: str,
    auth_headers,
    salon,
    db_session
):
    target_user = User(
        name="Target User",
        email="target-staff@example.com",
        password_hash="not-used",
        role="customer"
    )

    db_session.add(target_user)
    db_session.commit()
    db_session.refresh(target_user)

    res = client.post(
        "/staffs/",
        headers=auth_headers(customer_token),
        json={
            "user_id": target_user.id,
            "name": "Unauthorized Staff",
            "salon_id": salon.id
        }
    )

    assert res.status_code == 403


def test_admin_can_update_staff(
    client: TestClient,
    staff_profile,
    salon,
    admin_token: str,
    auth_headers
):
    res = client.patch(
        f"/staffs/{staff_profile.id}",
        headers=auth_headers(admin_token),
        json={
            "name": "Updated Staff",
            "salon_id": salon.id
        }
    )

    assert res.status_code == 200

    data = res.json()

    assert data["name"] == "Updated Staff"