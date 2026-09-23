"""initial migration

Revision ID: 18cf578b95de
Revises: 
Create Date: 2026-09-23 15:41:29.222538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = '18cf578b95de'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('salons',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('address', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_salons_id'), 'salons', ['id'], unique=False)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=255), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)
    op.create_index(op.f('ix_users_id'), 'users', ['id'], unique=False)
    op.create_table('customers',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_customers_id'), 'customers', ['id'], unique=False)
    op.create_table('menus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('price', sa.Integer(), nullable=False),
    sa.Column('duration_minutes', sa.Integer(), nullable=False),
    sa.Column('salon_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['salon_id'], ['salons.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_menus_id'), 'menus', ['id'], unique=False)
    op.create_table('staffs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('salon_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['salon_id'], ['salons.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_staffs_id'), 'staffs', ['id'], unique=False)
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('customer_id', sa.Integer(), nullable=False),
    sa.Column('staff_id', sa.Integer(), nullable=False),
    sa.Column('menu_id', sa.Integer(), nullable=False),
    sa.Column('start_at', sa.DateTime(), nullable=False),
    sa.Column('end_at', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['customer_id'], ['customers.id'], ),
    sa.ForeignKeyConstraint(['menu_id'], ['menus.id'], ),
    sa.ForeignKeyConstraint(['staff_id'], ['staffs.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_reservations_id'), 'reservations', ['id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_reservations_id'), table_name='reservations')
    op.drop_table('reservations')
    op.drop_index(op.f('ix_staffs_id'), table_name='staffs')
    op.drop_table('staffs')
    op.drop_index(op.f('ix_menus_id'), table_name='menus')
    op.drop_table('menus')
    op.drop_index(op.f('ix_customers_id'), table_name='customers')
    op.drop_table('customers')
    op.drop_index(op.f('ix_users_id'), table_name='users')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_salons_id'), table_name='salons')
    op.drop_table('salons')