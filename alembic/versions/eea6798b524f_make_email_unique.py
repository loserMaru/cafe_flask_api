"""Make email unique

Revision ID: eea6798b524f
Revises: 7c7e708a86a7
Create Date: 2024-02-18 17:29:17.108462

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eea6798b524f'
down_revision: Union[str, None] = '7c7e708a86a7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.execute('ALTER TABLE "user" ADD CONSTRAINT unique_email UNIQUE (email)')


# Определение функции отката миграции
def downgrade():
    op.execute('ALTER TABLE "user" DROP CONSTRAINT unique_email')
