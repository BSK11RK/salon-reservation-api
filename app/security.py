from datetime import datetime, timedelta, timezone

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from pwdlib import PasswordHash

from app.database import get_db
from app.models.user import User


password_hash = PasswordHash.recommended()

SECRET_KEY = "change-this-to-a-random-secret-key"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def hash_password(password: str) -> str:
    return password_hash.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return password_hash.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )
    
    payload = {"sub": str(user_id), "exp": expire}
    
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    
    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        
        user_id = payload.get("sub")
        
        if user_id is None:
            raise credentials_exception
        
        user_id = int(user_id)
        
    except (jwt.InvalidTokenError, ValueError):
        raise credentials_exception
    
    user = db.get(User, user_id)
    
    if user is None:
        raise credentials_exception
    
    return user


# Customer
def require_customer(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "customer":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Customer role required"
        )
        
    return current_user


# Staff
def require_staff(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "staff":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Staff role required"
        )

    return current_user


# Admin
def require_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin role required"
        )

    return current_user