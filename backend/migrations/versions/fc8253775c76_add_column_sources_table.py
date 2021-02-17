"""Add column sources table

Revision ID: fc8253775c76
Revises: b24f22c743a4
Create Date: 2021-02-17 17:19:04.872083

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc8253775c76'
down_revision = 'b24f22c743a4'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'column_source',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('column_id', sa.Integer, sa.ForeignKey('column.id')),
        sa.Column('source', sa.String(100), nullable=False),
        sa.Column('enabled', sa.Boolean(), nullable=False, default=True),
    )

def downgrade():
    op.drop_table('column_source')
