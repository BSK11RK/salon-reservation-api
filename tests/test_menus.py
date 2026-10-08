from fastapi.testclient import TestClient


def test_public_can_get_menus(
    client: TestClient,
):
    res = client.get("/menus/")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_admin_can_create_menu(
    client: TestClient,
    salon,
    admin_token: str,
    auth_headers
):
    res = client.post(
        "/menus/",
        headers=auth_headers(admin_token),
        json={
            "name": "Color",
            "price": 8000,
            "duration_minutes": 90,
            "salon_id": salon.id
        }
    )

    assert res.status_code == 201

    data = res.json()

    assert data["name"] == "Color"
    assert data["price"] == 8000
    assert data["duration_minutes"] == 90
    assert data["salon_id"] == salon.id


def test_customer_cannot_create_menu(
    client: TestClient,
    salon,
    customer_token: str,
    auth_headers
):
    res = client.post(
        "/menus/",
        headers=auth_headers(customer_token),
        json={
            "name": "Unauthorized Menu",
            "price": 5000,
            "duration_minutes": 60,
            "salon_id": salon.id
        }
    )

    assert res.status_code == 403


def test_admin_can_update_menu(
    client: TestClient,
    menu,
    admin_token: str,
    auth_headers
):
    res = client.patch(
        f"/menus/{menu.id}",
        headers=auth_headers(admin_token),
        json={"price": 6000}
    )

    assert res.status_code == 200

    data = res.json()

    assert data["price"] == 6000