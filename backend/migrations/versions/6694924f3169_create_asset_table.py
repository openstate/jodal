"""create asset table

Revision ID: 6694924f3169
Revises: 03904ff7ef41
Create Date: 2024-05-21 11:55:35.938049

"""
from alembic import op
import sqlalchemy as sa

try:
    from jodal.db import BinaryUUID
except Exception as e:
    pass

# revision identifiers, used by Alembic.
revision = '6694924f3169'
down_revision = '03904ff7ef41'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'asset',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('user_id', BinaryUUID),
        sa.Column('url', sa.String(1024), nullable=False),
        sa.Column('created', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('modified', sa.DateTime(), server_default=sa.func.current_timestamp()),
        sa.Column('last_run', sa.DateTime(), server_default=sa.func.current_timestamp())
    )


def downgrade():
    op.drop_table('asset')
