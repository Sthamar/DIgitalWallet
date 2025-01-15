"""deleted the payment table

Revision ID: 7e81432d2a14
Revises: b708787ec53f
Create Date: 2025-01-14 17:00:41.998935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '7e81432d2a14'
down_revision: Union[str, None] = 'b708787ec53f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('idx_status', table_name='payments')
    op.drop_index('idx_user_id', table_name='payments')
    op.drop_index('ix_payments_id', table_name='payments')
    op.drop_index('ix_payments_user_id', table_name='payments')
    op.drop_table('payments')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('payments',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('user_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('transaction_id', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('token', sa.VARCHAR(length=255), autoincrement=False, nullable=False),
    sa.Column('amount', sa.NUMERIC(precision=10, scale=2), autoincrement=False, nullable=False),
    sa.Column('status', postgresql.ENUM('PENDING', 'COMPLETED', 'FAILED', name='payment_status'), autoincrement=False, nullable=False),
    sa.Column('payment_method', sa.VARCHAR(length=50), autoincrement=False, nullable=True),
    sa.Column('created_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(), server_default=sa.text('now()'), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], name='payments_user_id_fkey', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name='payments_pkey'),
    sa.UniqueConstraint('transaction_id', name='payments_transaction_id_key')
    )
    op.create_index('ix_payments_user_id', 'payments', ['user_id'], unique=False)
    op.create_index('ix_payments_id', 'payments', ['id'], unique=False)
    op.create_index('idx_user_id', 'payments', ['user_id'], unique=False)
    op.create_index('idx_status', 'payments', ['status'], unique=False)
    # ### end Alembic commands ###
