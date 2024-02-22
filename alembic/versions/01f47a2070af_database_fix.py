"""Database fix

Revision ID: 01f47a2070af
Revises: eea6798b524f
Create Date: 2024-02-20 20:47:41.769752

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = '01f47a2070af'
down_revision: Union[str, None] = 'eea6798b524f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # Удаление столбца "location" из таблицы "coffee"
    op.drop_column('coffee', 'location')

    # Добавление внешнего ключа "cafe_id" в таблицу "coffee"
    op.add_column('coffee', sa.Column('cafe_id', sa.Integer, sa.ForeignKey('cafe.id')))

    # Удаление столбцов "count", "drink_type", "drinks_id" и "weight_id" из таблицы "order"
    op.drop_column('order', 'count')
    op.drop_column('order', 'drink_type')
    op.drop_column('order', 'drinks_id')
    op.drop_column('order', 'weight_id')

    # Удаление таблиц "dessert", "drinks", "products" и "weight"
    op.drop_table('products')
    op.drop_table('dessert')

    op.drop_column('weight', 'drinks_id')

    op.drop_table('drinks')
    op.drop_table('weight')

    # Создание таблицы "subscription" с полями "start_date", "end_date", "quantity" и связью с таблицей "user"
    op.create_table('subscription',
                    sa.Column('id', sa.Integer, primary_key=True),
                    sa.Column('start_date', sa.Date, nullable=False),
                    sa.Column('end_date', sa.Date, nullable=False),
                    sa.Column('quantity', sa.Integer, nullable=False),
                    sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'))
                    )


def downgrade():
    # Восстановление таблиц "dessert", "drinks", "products" и "weight"
    op.create_table('dessert',
                    sa.Column('id', sa.Integer, primary_key=True),
                    # Добавьте остальные столбцы таблицы "dessert" здесь
                    )
    op.create_table('drinks',
                    sa.Column('id', sa.Integer, primary_key=True),
                    # Добавьте остальные столбцы таблицы "drinks" здесь
                    )
    op.create_table('products',
                    sa.Column('id', sa.Integer, primary_key=True),
                    # Добавьте остальные столбцы таблицы "products" здесь
                    )
    op.create_table('weight',
                    sa.Column('id', sa.Integer, primary_key=True),
                    # Добавьте остальные столбцы таблицы "weight" здесь
                    )

    # Восстановление столбцов "count", "drink_type", "drinks_id" и "weight_id" в таблице "order"
    op.add_column('order', sa.Column('count', sa.Integer))
    op.add_column('order', sa.Column('drink_type', sa.String))
    op.add_column('order', sa.Column('drinks_id', sa.Integer))
    op.add_column('order', sa.Column('weight_id', sa.Integer))

    # Удаление внешнего ключа "cafe_id" из таблицы "coffee"
    op.drop_column('coffee', 'cafe_id')

    # Восстановление столбца "location" в таблице "coffee"
    op.add_column('coffee', sa.Column('location', sa.String))

    # Удаление таблицы "subscription"
    op.drop_table('subscription')
