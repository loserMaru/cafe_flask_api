"""Add user_id to order table

Revision ID: 6ed68196b972
Revises: 01f47a2070af
Create Date: 2024-02-20 21:39:25.135122

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6ed68196b972'
down_revision: Union[str, None] = '01f47a2070af'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('order', sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id')))


def downgrade() -> None:
    op.drop_column('order', 'user_id')

