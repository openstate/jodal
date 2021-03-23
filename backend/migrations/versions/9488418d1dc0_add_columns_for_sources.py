"""add columns for sources

Revision ID: 9488418d1dc0
Revises: ab9fb8dda135
Create Date: 2021-03-23 14:41:43.226930

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

# revision identifiers, used by Alembic.
revision = '9488418d1dc0'
down_revision = 'ab9fb8dda135'
branch_labels = None
depends_on = None

sources = ['poliflw','openspending', 'openbesluitvorming']

def upgrade():
    for s in sources:
        fld = 'src_%s' % (s,)
        op.add_column(
            'column', sa.Column(
                fld, sa.Boolean, server_default=expression.true(),
                nullable=False))


def downgrade():
    for s in sources:
        fld = 'src_%s' % (s,)
        op.drop_column('column', fld)
