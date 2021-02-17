"""create column table

Revision ID: 8a24e1c2174e
Revises:
Create Date: 2021-02-17 15:48:14.331925

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a24e1c2174e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'column',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('name', sa.String(100), nullable=False),
    )

def downgrade():
    op.drop_table('column')
