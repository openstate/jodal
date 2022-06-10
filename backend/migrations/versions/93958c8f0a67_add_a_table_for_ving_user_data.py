"""Add a table for ving user data

Revision ID: 93958c8f0a67
Revises: 73dc559925df
Create Date: 2022-06-10 15:08:33.381977

"""
from alembic import op
import sqlalchemy as sa


try:
    from jodal.db import BinaryUUID
except Exception as e:
    pass

# revision identifiers, used by Alembic.
revision = '93958c8f0a67'
down_revision = '73dc559925df'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'user_data',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', BinaryUUID),
        sa.Column('key', sa.String(100), nullable=False),
        sa.Column('value', sa.String(1024)),
    )


def downgrade():
    op.drop_table('user_data')
