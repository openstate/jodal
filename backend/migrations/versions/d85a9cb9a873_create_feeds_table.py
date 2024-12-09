"""create feeds table

Revision ID: d85a9cb9a873
Revises: 3c611a19088d
Create Date: 2024-12-04 15:07:06.508926

"""
from alembic import op
import sqlalchemy as sa

try:
    from jodal.db import BinaryUUID
except Exception as e:
    pass


# revision identifiers, used by Alembic.
revision = 'd85a9cb9a873'
down_revision = '3c611a19088d'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("feed",
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('public_id', sa.String(12), unique=True, index=True, nullable=False),
        sa.Column('user_id', BinaryUUID, nullable=False),
        sa.Column('name', sa.String(100), nullable=False),
        sa.Column('query', sa.String(100), nullable=False),
        sa.Column('locations', sa.String(1024), nullable=False),
        sa.Column('sources', sa.String(1024), nullable=False),
    )


def downgrade():
    op.drop_table('feed')
