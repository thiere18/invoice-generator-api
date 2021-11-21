from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP, BigInteger

from .database import Base


class Product(Base):
    __tablename__ = "products"
    id= Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity_init= Column(Integer(), nullable=True)
    # price=Column(BigInteger(), nullable=False),
    quantity_left= Column(Integer(), nullable=True)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)

 
class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, nullable=False)
    reference = Column(String(255), nullable=False)
    value_net= Column(BigInteger(), nullable=False)
    actual_payment = Column(BigInteger(), nullable=False)
    payment_due = Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    paid = Column(Boolean, server_default='False', nullable=False)
    deleted = Column(Boolean, server_default='False', nullable=False)
    invoice_owner_id = Column(Integer, ForeignKey(
        "users.id", ondelete="CASCADE"), nullable=False)
    items=relationship("InvoiceItem",backref="owner")
    pass

class InvoiceItem(Base):
    __tablename__ = "invoiceitems"
    id = Column(Integer, primary_key=True, nullable=False)
    product_name = Column(String(255), nullable=False)
    quantity= Column(Integer(), nullable=False)
    prix_unit= Column(BigInteger(), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    deleted = Column(Boolean, server_default='False', nullable=False)
    invoice_id = Column(Integer, ForeignKey(
        "invoices.id", ondelete="CASCADE"), nullable=False)
    


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(255), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True),
                        nullable=False, server_default=text('now()'))
    invoices=relationship("Invoice",backref="creator")
