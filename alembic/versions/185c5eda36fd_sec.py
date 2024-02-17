"""sec

Revision ID: 185c5eda36fd
Revises: 5cfdd730795f
Create Date: 2024-02-17 22:34:09.889166

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '185c5eda36fd'
down_revision: Union[str, None] = '5cfdd730795f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
