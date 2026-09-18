from sqlalchemy.orm import Session

from app.models.salon import Salon
from app.schemas.salon import SalonCreate, SalonUpdate


# GET
def get_salons(db: Session):
    return db.query(Salon).all()


# GET_ID
def get_salon(db: Session, salon_id: int):
    return db.get(Salon, salon_id)


# POST
def create_salon(db: Session, salon_data: SalonCreate):
    new_salon = Salon(
        name=salon_data.name,
        address=salon_data.address
    )
    
    db.add(new_salon)
    db.commit()
    db.refresh(new_salon)
    
    return new_salon


# PATCH
def update_salon(
    db: Session,
    salon_id: int,
    salon_data: SalonUpdate
):
    salon = db.get(Salon, salon_id)
    
    if salon is None:
        return None
    
    update_data = salon_data.model_dump(exclude_unset=True)
    
    for key, value in update_data.items():
        setattr(salon, key, value)
    
    db.commit()
    db.refresh(salon)
    
    return salon


# DELETE
def delete_salon(db: Session, salon_id: int):
    salon = db.get(Salon, salon_id)
    
    if salon is None:
        return None
    
    db.delete(salon)
    db.commit()
    
    return salon