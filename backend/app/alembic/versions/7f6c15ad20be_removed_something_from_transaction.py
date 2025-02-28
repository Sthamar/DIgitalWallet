"""removed something from transaction

Revision ID: 7f6c15ad20be
Revises: 0f7942acc1df
Create Date: 2025-01-15 20:51:01.538365

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f6c15ad20be'
down_revision: Union[str, None] = '0f7942acc1df'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('user_id', sa.Integer(), nullable=True))
    op.drop_constraint('transactions_receiver_user_id_fkey', 'transactions', type_='foreignkey')
    op.drop_constraint('transactions_sender_user_id_fkey', 'transactions', type_='foreignkey')
    op.create_foreign_key(None, 'transactions', 'users', ['user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('transactions', 'sender_user_id')
    op.drop_column('transactions', 'receiver_user_id')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('transactions', sa.Column('receiver_user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('transactions', sa.Column('sender_user_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'transactions', type_='foreignkey')
    op.create_foreign_key('transactions_sender_user_id_fkey', 'transactions', 'users', ['sender_user_id'], ['id'], ondelete='CASCADE')
    op.create_foreign_key('transactions_receiver_user_id_fkey', 'transactions', 'users', ['receiver_user_id'], ['id'], ondelete='CASCADE')
    op.drop_column('transactions', 'user_id')
    # ### end Alembic commands ###
