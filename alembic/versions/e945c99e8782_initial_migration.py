"""initial migration

Revision ID: e945c99e8782
Revises: 
Create Date: 2026-09-22 11:30:17.291595

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'e945c99e8782'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
