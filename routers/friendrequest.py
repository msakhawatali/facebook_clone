from fastapi import status, HTTPException, Depends, APIRouter
from oauth2 import get_current_active_user
from schemas import FriendRequestBase, FriendRequestUpdate
from sqlalchemy.orm import Session
from database import get_db
from sqlalchemy import or_
import models
import schemas

router = APIRouter(
    prefix="/friend_request",
    tags=['Friend_Request']
)

# Send Friend Request

@router.post("/", status_code=status.HTTP_200_OK)
async def send_friend_request(receiver_id : schemas.FriendRequestCreate, db : Session = Depends(get_db), current_user: schemas.Register= Depends(get_current_active_user)):
    find_receiver = db.query(models.Users).filter(models.Users.id == receiver_id.receiver_id).first()
    
    if find_receiver == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"receiver with id: {receiver_id} does not exist")

    existing_request = db.query(models.FriendRequest).filter(
        models.FriendRequest.sender_id == current_user.id,
        models.FriendRequest.receiver_id == receiver_id.receiver_id,
        models.FriendRequest.status == "pending"
    ).first()

    if existing_request:
        raise HTTPException(status_code=400,detail="Friend request already sent and is still pending")
    
    rejected_request = db.query(models.FriendRequest).filter(
        models.FriendRequest.status == "rejected"
    ).first()

    if rejected_request:
        raise HTTPException(status_code=400,detail=f"Friend request has already been rejected.")
    
     
    new_request = models.FriendRequest(
        sender_id = current_user.id,
        receiver_id = receiver_id.receiver_id
    )
    db.add(new_request)
    db.commit()
    db.refresh(new_request)
    return new_request

# Find received requests

@router.get("/received", response_model=list[FriendRequestBase], status_code=status.HTTP_200_OK)
async def get_all_received_requests(db : Session = Depends(get_db), current_user: schemas.Register= Depends(get_current_active_user)):
    requests = db.query(models.FriendRequest).filter(
        models.FriendRequest.receiver_id == current_user.id,
        models.FriendRequest.status == "Pending"
    )
    return requests

# Find send requests

@router.get("/send", response_model=list[FriendRequestBase], status_code=status.HTTP_200_OK)
async def get_all_send_requests(db : Session = Depends(get_db), current_user: schemas.Register= Depends(get_current_active_user)):
    requests = db.query(models.FriendRequest).filter(
        models.FriendRequest.sender_id == current_user.id,
        models.FriendRequest.status == "pending"
    ).all()

    if not requests:
        raise HTTPException(status_code=404,detail="You have not sent any pending friend requests.")

    return requests

# Accept/Reject a request

@router.put("/{friend_id}", response_model = schemas.FriendRequestUpdate ,status_code=status.HTTP_202_ACCEPTED)
async def Accept_Reject_request(friend_id : int, status_update : FriendRequestUpdate , db : Session = Depends(get_db), current_user : schemas.Register= Depends(get_current_active_user)):
    find_receiver = db.query(models.FriendRequest).filter(models.FriendRequest.id == friend_id).first()
    
    if find_receiver == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"receiver with id: {friend_id} does not exist")

    if find_receiver.status == "accepted":
        raise HTTPException(
            status_code=400,
            detail=f"Friend request with ID: {friend_id} is already accepted."
        )

    if find_receiver.status == "rejected":
        raise HTTPException(
            status_code=400,
            detail=f"Friend request with ID: {friend_id} has already been rejected."
        )

    find_receiver.status = status_update.status
    db.commit()
    db.refresh(find_receiver)
    return find_receiver

# List of accepted friends

@router.get("/friends_list", response_model=list[FriendRequestBase], status_code=status.HTTP_200_OK)
async def get_all_friend(db : Session = Depends(get_db), current_user: schemas.Register= Depends(get_current_active_user)):
    requests = db.query(models.FriendRequest).filter(
        or_(
            models.FriendRequest.sender_id == current_user.id,
            models.FriendRequest.receiver_id == current_user.id
        ),
        models.FriendRequest.status.ilike("accepted")
    ).all()
    return requests