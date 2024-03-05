"""Cafe and coffee added new row image

Revision ID: 6259394886c9
Revises: 754ff5c71925
Create Date: 2024-03-05 14:13:05.095494

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '6259394886c9'
down_revision: Union[str, None] = '754ff5c71925'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


# Определение функций для обновления и отката миграции
def upgrade():
    # Добавление поля image в таблицу cafe
    op.add_column('cafe', sa.Column('image', sa.TEXT(), nullable=True))

    # Добавление поля image в таблицу coffee
    op.add_column('coffee', sa.Column('image', sa.TEXT(), nullable=True))


def downgrade():
    # Удаление поля image из таблицы cafe
    op.drop_column('cafe', 'image')

    # Удаление поля image из таблицы coffee
    op.drop_column('coffee', 'image')
