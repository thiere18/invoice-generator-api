from fastapi import APIRouter, Depends
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.repository import auth
from .. import database, schemas

router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
def logs(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    return auth.login(db, user_credentials)
