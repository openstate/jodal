"""store binoas subscription

Revision ID: afb7fcef27c7
Revises: d85a9cb9a873
Create Date: 2025-01-27 10:53:30.497600

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'afb7fcef27c7'
down_revision = 'd85a9cb9a873'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column("feed", "query", type_=sa.String(1024))
    op.add_column("feed", sa.Column("binoas_feed_id", sa.String(100), nullable=True))
    op.add_column("feed", sa.Column("binoas_user_id", sa.Integer, nullable=True))
    op.add_column("feed", sa.Column("binoas_frequency", sa.String(100), nullable=True))

def downgrade():
    op.drop_column("feed", "binoas_frequency")
    op.drop_column("feed", "binoas_user_id")
    op.drop_column("feed", "binoas_feed_id")
    op.alter_column("feed", "query", type_=sa.String(100))
