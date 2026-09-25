"""Userにroleを追加

Revision ID: 7ca3dd29ff7e
Revises: 18cf578b95de
Create Date: 2026-09-25 14:01:28.031528

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '7ca3dd29ff7e'
down_revision: Union[str, Sequence[str], None] = '18cf578b95de'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "users",
        sa.Column(
            "role",
            sa.String(length=20),
            nullable=True,
        ),
    )

    # 既存Userはまず全員customerにする
    op.execute(
        "UPDATE users SET role = 'customer'"
    )

    # Staffに紐付いているUserはstaffにする
    op.execute(
        """
        UPDATE users
        SET role = 'staff'
        WHERE id IN (
            SELECT user_id
            FROM staffs
        )
        """
    )

    # roleを必須にする
    with op.batch_alter_table("users") as batch_op:
        batch_op.alter_column(
            "role",
            existing_type=sa.String(length=20),
            nullable=False,
        )


def downgrade() -> None:
    op.drop_column('users', 'role')