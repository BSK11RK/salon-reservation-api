from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.user import UserCreate, UserResponse
from app.services import user as user_service


router = APIRouter(prefix="/users", tags=["users"])


# POST
@router.post("/", response_model=UserResponse, status_code=201)
def create_user(user_data: UserCreate, db: Session = Depends(get_db)):
    user = user_service.create_user(db, user_data)
    
    if user is None:
        raise HTTPException(status_code=409, detail="Email already exists")
    
    return user