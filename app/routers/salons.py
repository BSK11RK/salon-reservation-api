from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.schemas.salon import SalonCreate, SalonUpdate
from app.services import salon as salon_service


router = APIRouter(prefix="/salons", tags=["Salons"])


# GET
@router.get("/")
def get_salons(db: Session = Depends(get_db)):
    return salon_service.get_salons(db)


# GET_ID
@router.get("/{salon_id}")
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    salon = salon_service.get_salon(db, salon_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return salon


# POST
@router.post("/")
def create_salon(salon: SalonCreate, db: Session = Depends(get_db)):
    return salon_service.create_salon(db, salon)


# PATCH
@router.patch("/{salon_id}")
def update_salon(
    salon_id: int,
    salon_data: SalonUpdate,
    db: Session = Depends(get_db)
):
    salon = salon_service.update_salon(db, salon_id, salon_data)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return salon


# DELETE
@router.delete("/{salon_id}")
def delete_salon(salo_id: int, db: Session = Depends(get_db)):
    salon = salon_service.delete_salon(db, salo_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return {"message": "Salon deleted successfully"}