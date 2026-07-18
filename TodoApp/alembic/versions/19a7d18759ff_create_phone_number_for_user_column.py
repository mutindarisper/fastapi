"""Create phone number for user column

Revision ID: 19a7d18759ff
Revises: 
Create Date: 2026-07-18 16:32:59.957335

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '19a7d18759ff'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
   op.add_column('users', sa.Column('phone_number', sa.String(), nullable=True)) #add a new column to the users table called phone_number


def downgrade() -> None:
    op.drop_column('users', 'phone_number')
