"""Изменение имени столбца time на time_order_made и добавление нового столбца pick_up_time

Revision ID: 144f42d0021e
Revises: 30764550b070
Create Date: 2024-04-14 19:17:46.631837

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '144f42d0021e'
down_revision: Union[str, None] = '30764550b070'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Имя таблицы
table_name = "order"


def upgrade():
    # Изменяем имя существующего столбца time на time_order_made
    op.alter_column(
        table_name,
        "time",
        new_column_name="time_order_made",
        existing_type=sa.DateTime(),
        existing_nullable=False
    )

    # Добавляем новый столбец pick_up_time
    op.add_column(
        table_name,
        sa.Column("pick_up_time", sa.DateTime(), nullable=True)
    )


def downgrade():
    # Удаляем новый столбец pick_up_time
    op.drop_column(table_name, "pick_up_time")

    # Изменяем имя столбца time_order_made обратно на time
    op.alter_column(
        table_name,
        "time_order_made",
        new_column_name="time",
        existing_type=sa.DateTime(),
        existing_nullable=False
    )
