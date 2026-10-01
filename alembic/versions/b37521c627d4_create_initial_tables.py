"""create initial tables

Revision ID: b37521c627d4
Revises: 
Create Date: 2026-10-01 14:52:23.756199

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'b37521c627d4'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass