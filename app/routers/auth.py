from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import LoginRequest, TokenResponse
from app.security import create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])


# POST
@router.post("/login", response_model=TokenResponse)
def login(login_data: LoginRequest, db: Session = Depends(get_db)):
    user = db.query(User).filter(
        User.email == login_data.email
    ).first()
    
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )
    
    if not verify_password(login_data.password, user.password_hash):
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )
        
    access_token = create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }