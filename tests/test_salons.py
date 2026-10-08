from fastapi.testclient import TestClient


def test_public_can_get_salons(client: TestClient):
    res = client.get("/salons/")

    assert res.status_code == 200
    assert isinstance(res.json(), list)


def test_public_can_get_salon(client: TestClient, salon):
    res = client.get(f"/salons/{salon.id}")

    assert res.status_code == 200

    data = res.json()

    assert data["id"] == salon.id
    assert data["name"] == "Test Salon"


def test_admin_can_update_salon(
    client: TestClient,
    salon,
    admin_token: str,
    auth_headers
):
    res = client.patch(
        f"/salons/{salon.id}",
        headers=auth_headers(admin_token),
        json={"name": "Updated Salon"}
    )

    assert res.status_code == 200

    data = res.json()

    assert data["name"] == "Updated Salon"


def test_customer_cannot_update_salon(
    client: TestClient,
    salon,
    customer_token: str,
    auth_headers
):
    res = client.patch(
        f"/salons/{salon.id}",
        headers=auth_headers(customer_token),
        json={"name": "Hacked Salon"}
    )

    assert res.status_code == 403