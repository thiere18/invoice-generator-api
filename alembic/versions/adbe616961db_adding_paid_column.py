"""adding  paid column

Revision ID: adbe616961db
Revises: d5253f495780
Create Date: 2021-11-25 12:05:44.981714

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'adbe616961db'
down_revision = 'd5253f495780'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('invoices', sa.Column('paid', sa.Boolean(), nullable=False,server_default=sa.text('False')))

    pass


def downgrade():
    pass
