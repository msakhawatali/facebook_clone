from fastapi import HTTPException, status
from passlib.context import CryptContext
from sqlalchemy.orm import Session
import models
import schemas

# Password Hashing Context Setup

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#  Password Verification Function

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Hashing Password Function

def hash_password(password: str):
    return pwd_context.hash(password)

# User Authentication Function

def authenticate_user(db: Session, username: str, password: str):
    user = db.query(models.Users).filter(models.Users.username == username).first()
    if not user or not verify_password(password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Invalid username or password")
    return user