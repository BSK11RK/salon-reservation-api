"""既存Staffユーザーのroleをstaffに更新

Revision ID: 816e1f960d3d
Revises: 7ca3dd29ff7e
Create Date: 2026-09-25 14:36:09.687063

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '816e1f960d3d'
down_revision: Union[str, Sequence[str], None] = '7ca3dd29ff7e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
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


def downgrade() -> None:
    op.execute(
        """
        UPDATE users
        SET role = 'customer'
        WHERE id IN (
            SELECT user_id
            FROM staffs
        )
        """
    )