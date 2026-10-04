"""add user phone number

Revision ID: ce94dbbe9d4a
Revises: aa0fe355ada8
Create Date: 2026-10-04 15:25:54.630858

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'ce94dbbe9d4a'
down_revision: Union[str, Sequence[str], None] = 'aa0fe355ada8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('users', sa.Column('phone_number', sa.String(length=20), nullable=True))
    

def downgrade() -> None:
    op.drop_column('users', 'phone_number')