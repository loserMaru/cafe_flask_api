"""Добавление столбца времени в таблицу order

Revision ID: 30764550b070
Revises: 7d5c44560a5f
Create Date: 2024-04-13 22:59:16.663466

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '30764550b070'
down_revision: Union[str, None] = '7d5c44560a5f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Имя таблицы
table_name = "order"


def upgrade():
    # Добавляем столбец времени в таблицу order
    op.add_column(
        table_name,
        sa.Column("time", sa.DateTime(), nullable=False, server_default=sa.func.now())
    )


def downgrade():
    # Удаляем столбец времени из таблицы order
    op.drop_column(table_name, "time")
