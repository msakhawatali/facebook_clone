from pydantic import BaseModel, EmailStr
from typing import Optional, TypeVar 
from datetime import datetime
from enum import Enum

T = TypeVar('T')

# create post

class PostBase(BaseModel):
    title : str
    content : str
    published : bool = True

class Post(PostBase):
    id: int
    created_at: datetime

class UserOut (BaseModel):
    id : int
    email : EmailStr
    created_at : datetime 
    class Config:
        from_attributes = True 

class PostCreate(PostBase):
    pass

    class Config:
        from_attributes = True

# Login

class LogIn(BaseModel):
    email : str
    password : str

# register

class CreateUser(BaseModel):
    username : str
    password : str
    email : Optional[EmailStr] = None
    phone_number : Optional[str] = None
    disabled : Optional[bool] = False
    

class Register(BaseModel):
    id : int 
    username : str
    email : Optional[EmailStr]
    phone_number : Optional[str]

    class Config:
        from_attributes = True

class UserInDB(Register):
    password : str

# User Login


class UserLogin(BaseModel):
    username: str
    password: str


# Token


class Token(BaseModel):
    access_token: str
    token_type: str 

class TokenData(BaseModel):
    username : str | None = None

# comment

class CommentBase(BaseModel):
    content: str

class CommentCreate(CommentBase):
    post_id: int

class CommentUpdate(CommentBase):
    pass

class CommentOut(CommentBase):
    id: int
    user_id: int
    timestamp: datetime

    class Config:
        from_attributes = True


# Friend request

class FriendStatus(str, Enum):
    pending = "pending"
    accepted = "accepted"
    rejected = "rejected"

class FriendRequestBase(BaseModel):
    sender_id : int
    receiver_id : int
    status: Optional[FriendStatus] = FriendStatus.pending

class FriendRequestCreate(BaseModel):
    receiver_id : int


class FriendRequestUpdate(BaseModel):
    status : FriendStatus

class FriendRequestOut(FriendRequestUpdate):
    id : int 
    sender_id : int
    receiver_id : int
    status : FriendStatus
    created_at : datetime

    class Config:
        from_attributes = True