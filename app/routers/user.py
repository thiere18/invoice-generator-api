from typing import List
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from app.repository import user
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_usr(users: schemas.UserCreate, db: Session = Depends(get_db)):
    return user.create_user(users, db)

@router.get('/{id}', response_model=schemas.UserInvoices)
def get_use(id: int, db: Session = Depends(get_db), ):
    return user.get_user(id, db)


@router.get('/', response_model=List[schemas.UserInvoices])
def get_user_all(db: Session = Depends(get_db)):
    return user.get_user_all(db)