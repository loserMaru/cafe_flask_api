"""third

Revision ID: 7c7e708a86a7
Revises: 185c5eda36fd
Create Date: 2024-02-17 22:38:35.579791

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c7e708a86a7'
down_revision: Union[str, None] = '185c5eda36fd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
