"""Add order for columns.

Revision ID: ab9fb8dda135
Revises: 0e3ba95ee33f
Create Date: 2021-02-23 15:34:47.359194

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ab9fb8dda135'
down_revision = '0e3ba95ee33f'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('column', sa.Column('order', sa.Integer, nullable=False, default=0))


def downgrade():
    op.drop_column('column', 'order')
