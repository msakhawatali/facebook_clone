from sqlalchemy import String, Integer, Column, Boolean, text, TIMESTAMP, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime

from database import Base, engine

# Database Tables Creation Function

def create_tables():
    Base.metadata.create_all(engine)

class FriendRequest(Base):
    __tablename__ = "friend_request"
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    receiver_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    status = Column(String, default=("pending"))
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))

class Comments(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow())
    post_id = Column(Integer, ForeignKey("post.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    post = relationship("Post", back_populates="comments")
    user = relationship("Users", back_populates="comments")

class Post(Base):
    __tablename__ = "post"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))
    comments = relationship("Comments", back_populates="post", cascade="all, delete")


class Users(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    email = Column(String)
    phone_number = Column(String)
    disabled = Column(Boolean, default=False)
    create_date = Column(TIMESTAMP(timezone=True),nullable=False, server_default=text("now()"))
    comments = relationship("Comments", back_populates="user", cascade="all, delete")
    


