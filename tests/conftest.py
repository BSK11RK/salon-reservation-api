import os

# ホスト側で pytest を実行した場合でも、
# app.database の DATABASE_URL が存在しないことで
# import error にならないようにする
#
# Docker内では compose.yaml から DATABASE_URL が渡されるため、
# こちらの値は使われない
os.environ.setdefault("DATABASE_URL", "sqlite://")


import pytest

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.security import hash_password

from app.models.salon import Salon
from app.models.staff import Staff
from app.models.menu import Menu
from app.models.customer import Customer
from app.models.reservation import Reservation
from app.models.user import User


TEST_PASSWORD = "password123"


@pytest.fixture
def db_session():
    """
    テスト専用のSQLiteインメモリDBを作成

    各テストごとに新しいDBを作成し、テスト終了後にテーブルを削除
    """

    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool
    )

    Base.metadata.create_all(bind=engine)

    TestingSessionLocal = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False
    )

    db = TestingSessionLocal()

    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db_session: Session):
    # FastAPIのDB依存をテスト専用DBに差し替える

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as test_client:
        yield test_client

    app.dependency_overrides.clear()


def create_test_user(
    db: Session,
    *,
    name: str,
    email: str,
    role: str
) -> User:
    # テスト用UserをDBへ直接作成

    user = User(
        name=name,
        email=email,
        password_hash=hash_password(TEST_PASSWORD),
        role=role
    )

    db.add(user)
    db.flush()

    return user


@pytest.fixture
def customer_user(db_session: Session):
    # Customer roleのUser

    user = create_test_user(
        db_session,
        name="Customer User",
        email="customer@example.com",
        role="customer"
    )

    db_session.commit()

    return user


@pytest.fixture
def admin_user(db_session: Session):
    # Admin roleのUser

    user = create_test_user(
        db_session,
        name="Admin User",
        email="admin@example.com",
        role="admin"
    )

    db_session.commit()

    return user


@pytest.fixture
def salon(db_session: Session):
    # テスト用Salon

    salon = Salon(name="Test Salon", address="Tokyo")

    db_session.add(salon)
    db_session.commit()
    db_session.refresh(salon)

    return salon


@pytest.fixture
def staff_user(db_session: Session, salon: Salon):
    # Staff roleのUserとStaffプロフィールを作成

    user = create_test_user(
        db_session,
        name="Staff User",
        email="staff@example.com",
        role="staff"
    )

    staff = Staff(
        user_id=user.id,
        name="Staff User",
        salon_id=salon.id
    )

    db_session.add(staff)
    db_session.commit()
    db_session.refresh(user)

    return user


@pytest.fixture
def staff_profile(db_session: Session, staff_user: User):
    # Staffのプロフィール

    return db_session.query(Staff).filter(
        Staff.user_id == staff_user.id
    ).first()


@pytest.fixture
def customer_profile(db_session: Session, customer_user: User):
    # CustomerのUserに対応するCustomerプロフィールを作成

    customer = Customer(user_id=customer_user.id, name="Customer User")

    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    return customer


@pytest.fixture
def other_customer_user(db_session: Session):
    # 別Customer用のUser

    user = create_test_user(
        db_session,
        name="Other Customer",
        email="other-customer@example.com",
        role="customer"
    )

    db_session.commit()

    return user


@pytest.fixture
def other_customer(db_session: Session, other_customer_user: User):
    # 別Customerのプロフィール

    customer = Customer(
        user_id=other_customer_user.id,
        name="Other Customer"
    )

    db_session.add(customer)
    db_session.commit()
    db_session.refresh(customer)

    return customer


@pytest.fixture
def menu(db_session: Session, salon: Salon):
    # テスト用Menu

    menu = Menu(
        name="Cut",
        price=5000,
        duration_minutes=60,
        salon_id=salon.id
    )

    db_session.add(menu)
    db_session.commit()
    db_session.refresh(menu)

    return menu


def login_user(client: TestClient, email: str) -> str:
    """
    テスト用ログイン処理
    パスワードはTEST_PASSWORDで統一
    """

    response = client.post(
        "/auth/login",
        data={
            "username": email,
            "password": TEST_PASSWORD
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


@pytest.fixture
def customer_token(client: TestClient, customer_profile: Customer):
    # Customerプロフィールが存在する状態でログイン

    return login_user(client, customer_profile.user.email)


@pytest.fixture
def staff_token(client: TestClient, staff_user: User):
    # Staffとしてログイン

    return login_user(client, staff_user.email)


@pytest.fixture
def admin_token(client: TestClient, admin_user: User):
    # Adminとしてログイン

    return login_user(client, admin_user.email)


@pytest.fixture
def auth_headers():
    # JWT認証用Headerを作る

    def create_headers(token: str):
        return {"Authorization": f"Bearer {token}"}

    return create_headers