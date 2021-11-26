from fastapi import status,Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
from .. import  schemas, oauth2
from ..database import get_db
from app.repository import invoice


router = APIRouter(
    prefix="/invoices",
    tags=['Invoices']
)


@router.get("/", response_model=List[schemas.InvoiceOut])
def get_invoices(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.get_invoices(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.InvoiceOut)
async def create_invoice(post: schemas.InvoiceCreate,item:List[schemas.InvoiceItem], db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.create_invoice(post,item,db,current_user)


@router.get("/{id}", response_model=schemas.InvoiceOut)
def get_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.get_invoice(id,db)


@router.put("/{id}", response_model=schemas.InvoiceOut)
def update_invoice(id: int, updated_post: schemas.InvoiceCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.update_invoice(id,updated_post,db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return invoice.delete_invoice(id, db)

