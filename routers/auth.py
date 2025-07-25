# Login
from fastapi import  status, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from oauth2 import ACCESS_TOKEN_EXPIRE_MINUTES
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
import schemas
import models
import oauth2
import utils

router = APIRouter(tags=["Authentication"])

# logIn
@router.post("/token", response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = utils.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Incorrect username or password", headers={"WWW-Authenticate": "Bearer"})
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = oauth2.create_access_token({"sub": user.username}, expires_delta= access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}