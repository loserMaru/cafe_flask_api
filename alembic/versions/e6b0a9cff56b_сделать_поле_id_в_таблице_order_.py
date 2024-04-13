"""Сделать поле id в таблице order автоинкрементируемым

Revision ID: e6b0a9cff56b
Revises: ca60885a91c4
Create Date: 2024-04-13 21:32:10.764392

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e6b0a9cff56b'
down_revision: Union[str, None] = 'ca60885a91c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

table_name = "order"


def upgrade():
    # Изменяем поле id на NOT NULL и устанавливаем автоинкрементирование
    op.alter_column(
        table_name,
        "id",
        existing_type=sa.Integer(),
        nullable=False,
        server_default=None,
        autoincrement=True
    )


def downgrade():
    # Отменяем автоинкрементирование для поля id
    op.alter_column(
        table_name,
        "id",
        existing_type=sa.Integer(),
        nullable=True,
        server_default=None,
        autoincrement=False
    )
