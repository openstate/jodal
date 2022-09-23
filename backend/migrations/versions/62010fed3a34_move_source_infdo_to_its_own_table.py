"""move source infdo to its own table.

Revision ID: 62010fed3a34
Revises: c0561da90538
Create Date: 2022-09-22 15:03:56.734146

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '62010fed3a34'
down_revision = 'c0561da90538'
branch_labels = None
depends_on = None

sources = ['poliflw','openspending', 'openbesluitvorming']

def upgrade():
    pass

def downgrade():
    pass
