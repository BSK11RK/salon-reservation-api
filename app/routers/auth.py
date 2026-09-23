from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.schemas.auth import TokenResponse
from app.security import create_access_token, verify_password


router = APIRouter(prefix="/auth", tags=["Auth"])


# POST
@router.post("/login", response_model=TokenResponse)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(
        User.email == form_data.username
    ).first()
    
    if user is None:
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )
    
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=401, 
            detail="Invalid email or password"
        )
        
    access_token = create_access_token(user.id)
    
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }