from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import func
# from sqlalchemy.sql.functions import func
from .. import models, schemas, oauth2
from ..database import get_db





def get_products(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    product=db.query(models.Product).filter(models.Product.deleted!=True).all()
    return  product


def create_product(post: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    new_product = models.Product(quantity_left=post.quantity_init,**post.dict())
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return new_product


def get_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} was not found")
    return product


def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product_query = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True)
    product = product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    product.deleted = True
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


def update_product(id: int, updated_post: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    product_query = db.query(models.Product).filter(models.Product.id == id,models.Product.deleted!=True)
    product = product_query.first()
    if product == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"product with id: {id} does not exist")
    product_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return product_query.first()