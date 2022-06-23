"""add a column to record read counts for a user.

Revision ID: c0561da90538
Revises: 93958c8f0a67
Create Date: 2022-06-22 13:23:34.633790

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c0561da90538'
down_revision = '93958c8f0a67'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('column', sa.Column('read_counts', sa.Text()))



def downgrade():
    op.drop_column('column', 'read_counts')
