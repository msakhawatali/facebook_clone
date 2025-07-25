from fastapi import status, HTTPException, Depends, Response, APIRouter
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas import Post
import models
import schemas
import oauth2

router = APIRouter(
    prefix="/post",
    tags=['Posts']
)


# Get Posts

@router.get("/", response_model=list[Post], status_code=status.HTTP_200_OK)
async def get_all_posts(db : Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts

# Create Posts

@router.post("/create_post", response_model=schemas.Post, status_code=status.HTTP_201_CREATED)
async def created_post(post : schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict())

    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# get one post

@router.get("/{post_id}", response_model=schemas.Post)
async def get_post(post_id : int, response : Response, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    return post

# Update Post

@router.put("/{post_id}",response_model=schemas.Post, status_code=status.HTTP_202_ACCEPTED)
async def updatepost(post_id : int, update_post : schemas.PostCreate, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    find_post = db.query(models.Post).filter(models.Post.id == post_id)
    post = find_post.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} does not exist")

    find_post.update(update_post.dict(), synchronize_session=False)
    db.commit()
    return find_post.first()

# Delete Post

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updatepost(post_id : int,  db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    find_post = db.query(models.Post).filter(models.Post.id == post_id)
    post = find_post.first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {post_id} does not exist")

    find_post.delete(synchronize_session=False)

    db.commit()

    return JSONResponse(
        content={"message" : "Your post successfully delete"},
        status_code=status.HTTP_200_OK
        )