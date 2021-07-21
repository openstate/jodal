"""Add additional columns to the column model.

Revision ID: 73dc559925df
Revises: 9488418d1dc0
Create Date: 2021-07-21 09:25:03.182567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '73dc559925df'
down_revision = '9488418d1dc0'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('column', sa.Column('sort', sa.String(16), server_default='published', nullable=False))
     op.add_column('column', sa.Column('sort_order', sa.String(4), server_default='desc', nullable=False))
     op.add_column('column', sa.Column('date_start', sa.DateTime))
     op.add_column('column', sa.Column('date_end', sa.DateTime))



def downgrade():
    op.drop_column('sort')
    op.drop_column('sort_order')
    op.drop_column('date_start')
    op.drop_column('date_end')
