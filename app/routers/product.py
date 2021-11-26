from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repository import product
from .. import models, schemas, oauth2
from ..database import get_db


router = APIRouter(
    prefix="/products",
    tags=['Products']
)


@router.get("/", response_model=List[schemas.ProductOut])
def get_products(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return product.get_products(db)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.ProductOut)
def create_product(post: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return product.create_product(post, db)


@router.get("/{id}", response_model=schemas.ProductOut)
def get_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return product.get_product(id,db)


@router.put("/{id}", response_model=schemas.ProductOut)
def update_product(id: int, updated_post: schemas.ProductCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return product.update_product(id,updated_post,db)


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    return product.delete_product(id,db)
