"""add star field to cafe

Revision ID: e32701340bf6
Revises: c36f419cda53
Create Date: 2024-04-08 18:23:18.199570

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = 'e32701340bf6'
down_revision: Union[str, None] = 'c36f419cda53'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Добавляем поле "star" типа "float" в таблицу "cafe"
    op.add_column('cafe', sa.Column('star', sa.Float(), nullable=True))


def downgrade():
    # Удаляем поле "star" из таблицы "cafe"
    op.drop_column('cafe', 'star')
