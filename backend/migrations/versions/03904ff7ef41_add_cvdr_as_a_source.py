"""add cvdr as a source.

Revision ID: 03904ff7ef41
Revises: 62010fed3a34
Create Date: 2022-09-23 11:55:59.255582

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import expression

# revision identifiers, used by Alembic.
revision = '03904ff7ef41'
down_revision = '62010fed3a34'
branch_labels = None
depends_on = None


sources = ['cvdr']

def upgrade():
    for s in sources:
        fld = 'src_%s' % (s,)
        op.add_column(
            'column', sa.Column(
                fld, sa.Boolean, server_default=expression.true(),
                nullable=False))


def downgrade():
    pass
    # for s in sources:
    #     fld = 'src_%s' % (s,)
    #     op.drop_column('column', fld)
