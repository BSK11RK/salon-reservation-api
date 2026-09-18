from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.staff import StaffCreate, StaffUpdate
from app.services import staff as staff_service


router = APIRouter(prefix="/staffs", tags=["Staffs"])


# GET
@router.get("/")
def get_staffs(db: Session = Depends(get_db)):
    return staff_service.get_staffs(db)


# GET_ID
@router.get("/{staff_id}")
def get_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = staff_service.get_staff(db, staff_id)
    
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    return staff


# POST
@router.post("/")
def create_staff(staff_data: StaffCreate, db: Session = Depends(get_db)):
    staff = staff_service.create_staff(db, staff_data)
    
    if staff is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return staff


# PATCH
@router.patch("/{staff_id}")
def update_staff(
    staff_id: int,
    staff_data: StaffUpdate,
    db: Session = Depends(get_db)
):
    staff = staff_service.update_staff(db, staff_id, staff_data)
    
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    return staff


# DELETE
@router.delete("/{staff_id}")
def delete_staff(staff_id: int, db: Session = Depends(get_db)):
    staff = staff_service.delete_staff(db, staff_id)
    
    if staff is None:
        raise HTTPException(status_code=404, detail="Staff not found")
    
    return {"message": "Staff deleted successfully"}