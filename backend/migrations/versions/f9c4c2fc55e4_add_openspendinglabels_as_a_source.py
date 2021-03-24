"""Add openspendinglabels as a source

Revision ID: f9c4c2fc55e4
Revises: 9488418d1dc0
Create Date: 2021-03-24 15:55:25.502253

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression


# revision identifiers, used by Alembic.
revision = 'f9c4c2fc55e4'
down_revision = '9488418d1dc0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'column', sa.Column(
            'src_openspendinglabels', sa.Boolean, server_default=expression.true(),
            nullable=False))


def downgrade():
    op.drop_column('column', 'src_openspendinglabels')
