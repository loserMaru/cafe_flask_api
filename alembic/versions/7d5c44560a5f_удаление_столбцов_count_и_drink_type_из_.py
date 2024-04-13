"""Удаление столбцов count и drink_type из таблицы order

Revision ID: 7d5c44560a5f
Revises: e6b0a9cff56b
Create Date: 2024-04-13 22:18:53.991164

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '7d5c44560a5f'
down_revision: Union[str, None] = 'e6b0a9cff56b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "order"


def upgrade():
    # Удаляем столбец count
    op.drop_column(table_name, "count")

    # Удаляем столбец drink_type
    op.drop_column(table_name, "drink_type")


def downgrade():
    # Добавляем столбец count обратно
    op.add_column(
        table_name,
        sa.Column("count", sa.Integer(), nullable=True)
    )

    # Добавляем столбец drink_type обратно
    op.add_column(
        table_name,
        sa.Column("drink_type", sa.String(length=255), nullable=True)
    )
