from sqlalchemy.orm import Session

from app.models.salon import Salon
from app.models.staff import Staff
from app.models.user import User
from app.schemas.staff import StaffCreate, StaffUpdate


# GET
def get_staffs(db: Session):
    return db.query(Staff).all()


# GET_ID
def get_staff(db: Session, staff_id: int):
    return db.get(Staff, staff_id)


# POST
def create_staff(db: Session, staff_data: StaffCreate):
    user = db.get(User, staff_data.user_id)
    
    if user is None:
        return "user_not_found"
    
    existing_staff = db.query(Staff).filter(
        Staff.user_id == staff_data.user_id
    ).first()
    
    if existing_staff is not None:
        return "staff_exists"
    
    salon = db.get(Salon, staff_data.salon_id)
    
    if salon is None:
        return "salon_not_found"
    
    new_staff = Staff(
        user_id=staff_data.user_id,
        name=staff_data.name,
        salon_id=staff_data.salon_id
    )
    
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)
    
    return new_staff


# PATCH
def update_staff(
    db: Session,
    staff_id: int,
    staff_data: StaffUpdate
):
    staff = db.get(Staff, staff_id)
    
    if staff is None:
        return None
    
    update_data = staff_data.model_dump(exclude_unset=True)
    
    if "salon_id" is update_data:
        salon = db.get(Salon, update_data["salon_id"])
        
        if salon is None:
            return "salon_not_found"
    
    for key, value in update_data.items():
        setattr(staff, key, value)
        
    db.commit()
    db.refresh(staff)
    
    return staff


# DELETE
def delete_staff(db: Session, staff_id: int):
    staff = db.get(Staff, staff_id)

    if staff is None:
        return None

    db.delete(staff)
    db.commit()

    return staff