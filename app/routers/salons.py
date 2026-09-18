from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.models.salon import Salon
from app.schemas.salon import SalonCreate, SalonUpdate


router = APIRouter(prefix="/salons", tags=["Salons"])


# GET
@router.get("/")
def get_salons(db: Session = Depends(get_db)):
    return db.query(Salon).all()


# GET_ID
@router.get("/{salon_id}")
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    salon = db.get(Salon, salon_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return salon


# POST
@router.post("/")
def create_salon(salon: SalonCreate, db: Session = Depends(get_db)):
    new_salon = Salon(
        name=salon.name,
        address=salon.address
    )
    
    db.add(new_salon)
    db.commit()
    db.refresh(new_salon)
    
    return new_salon


# PATCH
@router.patch("/{salon_id}")
def update_salon(
    salon_id: int,
    salon_data: SalonUpdate,
    db: Session = Depends(get_db)
):
    salon = db.get(Salon, salon_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    update_date = salon_data.model_dump(exclude_unset=True)
    
    for key, Value in update_date.items():
        setattr(salon, key, Value)
        
    db.commit()
    db.refresh(salon)
    
    return salon


# DELETE
@router.delete("/{salon_id}")
def delete_salon(salo_id: int, db: Session = Depends(get_db)):
    salon = db.get(Salon, salo_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    db.delete(salon)
    db.commit()
    
    return {"message": "Salon deleted successfully"}