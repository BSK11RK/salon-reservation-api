from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services import user as user_service
from app.security import get_current_user


router = APIRouter(prefix="/users", tags=["users"])


# GET
@router.get("/", response_model=list[UserResponse])
def get_user(db: Session = Depends(get_db)):
    return user_service.get_users(db)


# GET_ME
@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user


# GET_ID
@router.get("/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.get_user(db, user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user


# POST
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, user_data)
    
    if user is None:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    return user


# PATCH
@router.patch("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int,
    user_data: UserUpdate,
    db: Session = Depends(get_db)
):
    user = user_service.update_user(db, user_id, user_data)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    if user == "email_exists":
        raise HTTPException(status_code=409, detail="Email already exists")
    
    return user


# DELETE
@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = user_service.delete_user(db, user_id)
    
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {"message": "User deleted successfully"}