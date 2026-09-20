from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate
from app.security import hash_password


# GET
def get_users(db: Session):
    return db.query(User).all()


# GET_ID
def get_user(db: Session, user_id: int):
    return db.get(User, user_id)


# POST
def create_user(db: Session, user_data: UserCreate):
    existing_user = db.query(User).filter(
        User.email == user_data.email
    ).first()
    
    if existing_user is not None:
        return None
    
    new_user = User(
        name=user_data.name,
        email=user_data.email,
        password_hash=hash_password(user_data.password)
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user