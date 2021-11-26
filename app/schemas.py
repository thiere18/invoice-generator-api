from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import List, Optional

from pydantic.types import conint
    
#product schemas

class Product(BaseModel):
    product_name:str
    # price:int
    quantity_init: int
    

class ProductCreate(Product):
    pass

class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


    class Config:
        orm_mode = True
      
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None

class Product(BaseModel):
    id: int
    product_name: str
    # price:int
    quantity_init: int
    quantity_left:int
    created_at: datetime
    class Config:
        orm_mode = True


class ProductOut(BaseModel):
    id: int
    product_name: str
    # price:int
    quantity_init: int
    quantity_left:int
    created_at: datetime
    class Config:
        orm_mode = True

# invoice schemas
class InvoiceItem(BaseModel):
    product_name:str
    quantity:int
    prix_unit:int
class InvoiceItemOut(BaseModel):
    id:int
    product_name:str
    quantity:int
    prix_unit:int
    created_at:datetime
    class Config:
        orm_mode = True
    
class Invoice(BaseModel):
    reference:str
    value_net: int
    actual_payment: int
    pass

class InvoiceCreate(Invoice):
    pass
    
class InvoiceOut(BaseModel):
    id:int
    reference:str
    value_net: int
    payment_due: int
    actual_payment: int
    invoice_owner_id:int
    paid:bool
    created_at: datetime
    items:List[InvoiceItemOut]
    class Config:
        orm_mode = True
 
class UserInvoices(BaseModel):
    # id: int
    username:str
    email: EmailStr
    created_at: datetime
    invoices:list[InvoiceOut]
    class Config:
        orm_mode = True
        
        
