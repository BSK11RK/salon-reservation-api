from fastapi.testclient import TestClient


def test_customer_cannot_get_all_users(
    client: TestClient,
    customer_token: str,
    auth_headers
):
    res = client.get(
        "/users/",
        headers=auth_headers(customer_token)
    )

    assert res.status_code == 403


def test_staff_cannot_get_all_users(
    client: TestClient,
    staff_token: str,
    auth_headers
):
    res = client.get(
        "/users/",
        headers=auth_headers(staff_token)
    )

    assert res.status_code == 403


def test_admin_can_get_all_users(
    client: TestClient,
    admin_token: str,
    auth_headers
):
    res = client.get(
        "/users/",
        headers=auth_headers(admin_token)
    )

    assert res.status_code == 200


def test_customer_cannot_create_salon(
    client: TestClient,
    customer_token: str,
    auth_headers
):
    res = client.post(
        "/salons/",
        headers=auth_headers(customer_token),
        json={
            "name": "Unauthorized Salon",
            "address": "Tokyo"
        }
    )

    assert res.status_code == 403


def test_staff_cannot_create_salon(
    client: TestClient,
    staff_token: str,
    auth_headers
):
    res = client.post(
        "/salons/",
        headers=auth_headers(staff_token),
        json={
            "name": "Unauthorized Salon",
            "address": "Tokyo"
        }
    )

    assert res.status_code == 403


def test_admin_can_create_salon(
    client: TestClient,
    admin_token: str,
    auth_headers
):
    res = client.post(
        "/salons/",
        headers=auth_headers(admin_token),
        json={
            "name": "Admin Salon",
            "address": "Tokyo"
        }
    )

    assert res.status_code == 201