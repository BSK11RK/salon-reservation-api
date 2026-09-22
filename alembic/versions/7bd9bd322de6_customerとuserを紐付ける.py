"""CustomerとUserを紐付ける

Revision ID: 7bd9bd322de6
Revises: e945c99e8782
Create Date: 2026-09-22 21:28:05.313372

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "7bd9bd322de6"
down_revision: Union[str, Sequence[str], None] = "e945c99e8782"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # 1. user_idを一旦NULL許可で追加
    op.add_column(
        "customers",
        sa.Column(
            "user_id",
            sa.Integer(),
            nullable=True,
        )
    )
    # 2. 既存CustomerとUserをemailで紐付ける
    connection = op.get_bind()

    connection.execute(
        sa.text(
            """
            UPDATE customers
            SET user_id = (
                SELECT users.id
                FROM users
                WHERE users.email = customers.email
            )
            """
        )
    )
    # 3. Userと紐付けられなかったCustomerがないか確認
    result = connection.execute(
        sa.text(
            """
            SELECT COUNT(*)
            FROM customers
            WHERE user_id IS NULL
            """
        )
    )

    unmatched_count = result.scalar()

    if unmatched_count != 0:
        raise RuntimeError("Userと紐付けられないCustomerが存在します。")

    # 4. user_idをNOT NULLに変更
    with op.batch_alter_table("customers") as batch_op:
        batch_op.alter_column(
            "user_id",
            existing_type=sa.Integer(),
            nullable=False
        )
        # 5. UserとCustomerを1対1にする
        batch_op.create_unique_constraint(
            "uq_customers_user_id",
            ["user_id"]
        )
        # 6. Userへの外部キーを作る
        batch_op.create_foreign_key(
            "fk_customers_user_id_users",
            "users",
            ["user_id"],
            ["id"]
        )
        # 7. Customerのemail indexを削除
        batch_op.drop_index("ix_customers_email")
        # 8. Customerからemailを削除
        batch_op.drop_column("email")


def downgrade() -> None:
    # 戻す場合はemailをNULL許可で復元
    with op.batch_alter_table("customers") as batch_op:
        batch_op.add_column(
            sa.Column(
                "email",
                sa.String(length=255),
                nullable=True
            )
        )
        batch_op.drop_constraint(
            "fk_customers_user_id_users",
            type_="foreignkey"
        )
        batch_op.drop_constraint("uq_customers_user_id", type_="unique")
        batch_op.create_index(
            "ix_customers_email",
            ["email"],
            unique=True
        )
        batch_op.drop_column("user_id")