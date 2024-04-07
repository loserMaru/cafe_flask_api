"""Change password field length

Revision ID: 6270bda06fee
Revises: 6259394886c9
Create Date: 2024-04-07 21:42:56.927842

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6270bda06fee'
down_revision: Union[str, None] = '6259394886c9'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('user', 'password', type_=sa.String(length=255))


def downgrade() -> None:
    pass
