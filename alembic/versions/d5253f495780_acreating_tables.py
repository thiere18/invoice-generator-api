"""acreating tables

Revision ID: d5253f495780
Revises: 
Create Date: 2021-11-21 13:34:47.892501

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5253f495780'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('invoices', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('reference', sa.String(), nullable=False),
                    sa.Column('value_net', sa.BigInteger(), nullable=False),
                    sa.Column('actual_payment',sa.BigInteger(), nullable=False),
                    sa.Column('payment_due',sa.BigInteger(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,server_default=sa.text('False'),),
                    sa.PrimaryKeyConstraint('id'),

                    )
    op.create_table('products',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('product_name', sa.String(), nullable=False),
                    sa.Column('quantity_left',sa.Integer(), nullable=True),
                    sa.Column('quantity_init',sa.Integer(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,server_default=sa.text('False'),),
                    sa.PrimaryKeyConstraint('id'),
                    )
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('username', sa.String(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,server_default=sa.text('False'),),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'),
                    )
    op.create_table('invoiceitems', 
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('product_name', sa.String(), nullable=False),
                    sa.Column('quantity',sa.Integer(),nullable=False),
                    sa.Column('prix_unit',sa.BigInteger(),nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.Column('deleted', sa.Boolean(), nullable=False,server_default=sa.text('False'),),
                    sa.PrimaryKeyConstraint('id'),
                    )
    
    op.add_column('invoiceitems', sa.Column('invoice_id', sa.Integer(), nullable=False))
    op.create_foreign_key('invoiceitems_invoice_fk', source_table="invoiceitems", referent_table="invoices", local_cols=[
                          'invoice_id'], remote_cols=['id'], ondelete="CASCADE")
    
    op.add_column('invoices', sa.Column('invoice_owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('invoices_user_fk', source_table="invoices", referent_table="users", local_cols=[
                          'invoice_owner_id'], remote_cols=['id'], ondelete="CASCADE")
    
    pass


def downgrade():
    pass
