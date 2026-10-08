from datetime import datetime

from fastapi.testclient import TestClient
from app.models.reservation import Reservation


def create_reservation(
    client: TestClient,
    token: str,
    staff_id: int,
    menu_id: int,
    start_at: str,
    auth_headers
):
    # Customerとして予約を作成する共通処理

    return client.post(
        "/reservations/",
        headers=auth_headers(token),
        json={
            "staff_id": staff_id,
            "menu_id": menu_id,
            "start_at": start_at
        }
    )


def test_customer_can_create_reservation(
    client: TestClient,
    customer_profile,
    staff_profile,
    menu,
    customer_token: str,
    auth_headers
):
    # Customerは予約を作成

    response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert response.status_code == 200

    data = response.json()

    # Reservation本体
    assert data["id"] is not None
    assert data["start_at"] is not None
    assert data["end_at"] is not None

    # 関連Customer
    assert data["customer"]["id"] == customer_profile.id

    # 関連Staff
    assert data["staff"]["id"] == staff_profile.id

    # 関連Menu
    assert data["menu"]["id"] == menu.id


def test_customer_can_get_own_reservation(
    client: TestClient,
    customer_profile,
    staff_profile,
    menu,
    customer_token: str,
    auth_headers
):
    # Customerは自分の予約を取得

    create_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert create_response.status_code == 200

    reservation_id = create_response.json()["id"]

    response = client.get(
        f"/reservations/{reservation_id}",
        headers=auth_headers(customer_token)
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reservation_id
    assert data["customer"]["id"] == customer_profile.id


def test_customer_cannot_get_other_customer_reservation(
    client: TestClient,
    db_session,
    customer_profile,
    other_customer,
    staff_profile,
    menu,
    customer_token: str,
    auth_headers
):
    # Customerは他のCustomerの予約を取得できない

    reservation = Reservation(
        customer_id=other_customer.id,
        staff_id=staff_profile.id,
        menu_id=menu.id,
        start_at=datetime(2026, 1, 1, 10, 0),
        end_at=datetime(2026, 1, 1, 11, 0)
    )

    db_session.add(reservation)
    db_session.commit()
    db_session.refresh(reservation)

    response = client.get(
        f"/reservations/{reservation.id}",
        headers=auth_headers(customer_token)
    )

    assert response.status_code == 404


def test_staff_can_get_own_reservations(
    client: TestClient,
    staff_profile,
    menu,
    customer_token: str,
    staff_token: str,
    auth_headers
):
    # Staffは自分が担当する予約を見ることができる

    create_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert create_response.status_code == 200

    response = client.get(
        "/reservations/staff/me",
        headers=auth_headers(staff_token)
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["staff"]["id"] == staff_profile.id


def test_admin_can_get_all_reservations(
    client: TestClient,
    staff_profile,
    menu,
    customer_token: str,
    admin_token: str,
    auth_headers
):
    # Adminは全予約を取得

    create_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert create_response.status_code == 200

    response = client.get(
        "/reservations/",
        headers=auth_headers(admin_token)
    )

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1


def test_customer_can_update_own_reservation(
    client: TestClient,
    staff_profile,
    menu,
    customer_token: str,
    auth_headers
):
    # Customerは自分の予約を変更

    create_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert create_response.status_code == 200

    reservation_id = create_response.json()["id"]

    response = client.patch(
        f"/reservations/{reservation_id}",
        headers=auth_headers(customer_token),
        json={"start_at": "2026-01-01T12:00:00"}
    )

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == reservation_id


def test_customer_can_delete_own_reservation(
    client: TestClient,
    staff_profile,
    menu,
    customer_token: str,
    auth_headers
):
    # Customerは自分の予約を削除

    create_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert create_response.status_code == 200

    reservation_id = create_response.json()["id"]

    response = client.delete(
        f"/reservations/{reservation_id}",
        headers=auth_headers(customer_token)
    )

    assert response.status_code == 200


def test_reservation_time_conflict(
    client: TestClient,
    staff_profile,
    menu,
    customer_token: str,
    auth_headers
):
    # 同じStaffの時間が重複する予約は作成できない

    first_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert first_response.status_code == 200

    second_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:30:00",
        auth_headers
    )

    assert second_response.status_code == 409


def test_adjacent_reservations_are_allowed(
    client: TestClient,
    staff_profile,
    menu,
    customer_token: str,
    auth_headers
):
    first_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T10:00:00",
        auth_headers
    )

    assert first_response.status_code == 200

    second_response = create_reservation(
        client,
        customer_token,
        staff_profile.id,
        menu.id,
        "2026-01-01T11:00:00",
        auth_headers
    )

    assert second_response.status_code == 200