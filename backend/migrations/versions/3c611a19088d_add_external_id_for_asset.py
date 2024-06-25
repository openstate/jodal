"""add external id for asset

Revision ID: 3c611a19088d
Revises: 6694924f3169
Create Date: 2024-06-25 13:44:23.690967

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3c611a19088d'
down_revision = '6694924f3169'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('asset', sa.Column('external_id', sa.String(100)))


def downgrade():
    op.drop_column('asset', 'user_id')
