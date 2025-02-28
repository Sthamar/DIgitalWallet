"""removed something from transaction

Revision ID: 51ab151abbff
Revises: 26a610e4fc78
Create Date: 2025-01-15 20:56:50.640526

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '51ab151abbff'
down_revision: Union[str, None] = '26a610e4fc78'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('user_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'transactions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.drop_column('transactions', 'user_id')
    # ### end Alembic commands ###
