from fastapi import status, HTTPException, Depends, APIRouter
from fastapi.responses import JSONResponse
from oauth2 import get_current_active_user
from sqlalchemy.orm import Session
from database import get_db
import models
import schemas

router = APIRouter(
    prefix="/comment",
    tags=['Comments']
)

# create comment

@router.post("/create_comment", response_model=schemas.CommentOut)
async def create_comment(comment: schemas.CommentCreate, db : Session = Depends(get_db), current_user: schemas.Register= Depends(get_current_active_user)):
    post = db.query(models.Post).filter(models.Post.id == comment.post_id).first()
    
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {comment.post_id} does not exist")
    
    new_comment = models.Comments(
        content=comment.content,
        post_id=comment.post_id,
        user_id=current_user.id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# Update Comment

@router.put("/update_comment/{comment_id}",response_model=schemas.CommentOut, status_code=status.HTTP_202_ACCEPTED)
async def updatecomment(comment_id : int, update_comment : schemas.CommentUpdate, db : Session = Depends(get_db), current_user: schemas.Register= Depends(get_current_active_user)):
    find_comment = db.query(models.Comments).filter(models.Comments.id == comment_id)
    comment = find_comment.first()
    
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment with id: {comment_id} does not exist")

    find_comment.update(update_comment.dict(), synchronize_session=False)
    db.commit()
    return find_comment.first()

# Delete Comment

@router.delete("/delete_comment/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def updatepost(comment_id : int,  db : Session = Depends(get_db), current_user: schemas.Register= Depends(get_current_active_user)):
    find_comment = db.query(models.Comments).filter(models.Comments.id == comment_id)
    comment = find_comment.first()
    
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"comment with id: {comment_id} does not exist")

    find_comment.delete(synchronize_session=False)
    db.commit()
    return JSONResponse(
        content={"message" : "Your comment successfully delete"},
        status_code=status.HTTP_200_OK
        )