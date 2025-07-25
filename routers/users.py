from fastapi import  status, HTTPException, Depends, Response, APIRouter
from database import SessionLocal, get_db, engine
from oauth2 import get_current_active_user
from sqlalchemy.orm import Session
from datetime import timedelta
import utils
import schemas
import models
import oauth2

router = APIRouter(
    prefix="/users",
    tags=['Users']
)


# Register 

@router.post("/signup", response_model=schemas.Register)
async def signup(user: schemas.CreateUser, db: Session = Depends(get_db)):
    # username = user.username.strip().lower()

    if db.query(models.Users).filter(models.Users.email == user.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = utils.hash_password(user.password)
    new_user = models.Users(username=user.username, password=hashed_password, email=user.email, phone_number=user.phone_number)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



# Current Logged-in User Endpoint

@router.get("/me/", response_model=schemas.Register)
async def read_users_me(current_user: schemas.Register= Depends(get_current_active_user)):
    return current_user

# User's Own Items Endpoint

@router.get("/me/item")
async def read_own_item(current_user: schemas.Register= Depends(get_current_active_user)):
    return [{"item_id": current_user.id, "owner": current_user}]
