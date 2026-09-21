from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
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


# PATCH
def update_user(
    db: Session,
    user_id: int,
    user_data: UserUpdate
):
    user = db.get(User, user_id)
    
    if user is None:
        return None
    
    update_data = user_data.model_dump(exclude_unset=True)
    
    if "email" in update_data:
        existing_user = db.query(User).filter(
            User.email == update_data["email"],
            User.id != user_id
        ).first()
        
        if existing_user is not None:
            return "email_exists"
        
    if "password" in update_data:
        update_data["password_hash"] = hash_password(
            update_data.pop("password")
        )
        
    for key, value in update_data.items():
        setattr(user, key, value)
        
    db.commit()
    db.refresh(user)
    
    return user
    
    
# DELETE
def delete_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    
    if user is None:
        return None
    
    db.delete(user)
    db.commit()
    
    return user