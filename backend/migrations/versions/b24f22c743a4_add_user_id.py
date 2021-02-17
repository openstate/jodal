"""Add user id

Revision ID: b24f22c743a4
Revises: 8a24e1c2174e
Create Date: 2021-02-17 16:44:54.295290

"""
from alembic import op
import sqlalchemy as sa

from jodal.db import BinaryUUID


# revision identifiers, used by Alembic.
revision = 'b24f22c743a4'
down_revision = '8a24e1c2174e'
branch_labels = None
depends_on = None


def upgrade():
     op.add_column('column', sa.Column('user_id', BinaryUUID))


def downgrade():
    op.drop_column('column', 'user_id')
