from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
import asyncio
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db




def get_invoices(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    containers=db.query(models.Invoice).filter(models.Invoice.deleted!=True).all()
    return  containers


async def create_invoice(post: schemas.InvoiceCreate,item:List[schemas.InvoiceItem], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
 
    new_invoice = models.Invoice(invoice_owner_id=current_user.id,payment_due=(post.value_net-post.actual_payment), **post.dict())
    db.add(new_invoice)
    db.commit()
    db.refresh(new_invoice)
    
    new_id=new_invoice.id
    for invoice_item in item:
        prod=invoice_item.product_name
        quant=invoice_item.quantity
        #verify if this product exist
        p= db.query(models.Product).filter(models.Product.product_name==prod).first()
        if not p:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST ,detail=f"{prod} is not a product")
        p.quantity_left-=quant
        db.commit()
        new_invoice_item = models.InvoiceItem(invoice_id=new_id,**invoice_item.dict())
        db.add(new_invoice_item)
        db.commit()
    
    return new_invoice



def get_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
  

    invoice = db.query(models.Invoice).filter(models.Invoice.id == id,models.Invoice.deleted!=True).first()

    if not invoice:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invoice with id: {id} was not found")

    return invoice


def update_invoice(id: int, updated_post: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    invoice_query = db.query(models.Invoice).filter(models.Invoice.id == id,models.Invoice.deleted!=True)

    invoice = invoice_query.first()

    if invoice == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invoice with id: {id} does not exist")

    
    invoice_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()

    return invoice_query.first()

def delete_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    invoice_query = db.query(models.Invoice).filter(models.Invoice.id == id,models.Invoice.deleted!=True)

    invoice = invoice_query.first()

    if invoice == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"invoice with id: {id} does not exist")
    invoice.deleted = True
  
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)




#