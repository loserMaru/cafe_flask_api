"""Добавление поля user_id в таблицу order

Revision ID: ca60885a91c4
Revises: c36f419cda53
Create Date: 2024-04-13 21:23:35.867546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'ca60885a91c4'
down_revision: Union[str, None] = 'c36f419cda53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "order"
column_name = "user_id"


def upgrade():
    # Добавляем поле user_id в таблицу order
    op.add_column(
        table_name,
        sa.Column(column_name, sa.Integer(), sa.ForeignKey("user.id"), nullable=False)
    )


def downgrade():
    # Удаляем поле user_id из таблицы order
    op.drop_column(table_name, column_name)
