"""add phone to users

Revision ID: de2f0564cddc
Revises: b37521c627d4
Create Date: 2026-10-01 14:57:32.421153

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'de2f0564cddc'
down_revision: Union[str, Sequence[str], None] = 'b37521c627d4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone', sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column('users', 'phone')