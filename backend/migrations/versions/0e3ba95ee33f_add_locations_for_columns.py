"""Add locations for columns.

Revision ID: 0e3ba95ee33f
Revises: fc8253775c76
Create Date: 2021-02-23 12:35:49.090554

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0e3ba95ee33f'
down_revision = 'fc8253775c76'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('column', sa.Column('locations', sa.String(1024)))


def downgrade():
    op.drop_column('column', 'locations')
