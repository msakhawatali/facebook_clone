from fastapi import FastAPI
from database import engine
from models import Base
from routers import users, auth, posts, comments, friendrequest

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(posts.router)
app.include_router(comments.router)
app.include_router(friendrequest.router)