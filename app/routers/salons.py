from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import require_admin
from app.schemas.salon import SalonCreate, SalonUpdate, SalonResponse
from app.services import salon as salon_service


router = APIRouter(prefix="/salons", tags=["Salons"])


# GET
@router.get("/", response_model=list[SalonResponse])
def get_salons(db: Session = Depends(get_db)):
    return salon_service.get_salons(db)


# GET_ID
@router.get("/{salon_id}", response_model=SalonResponse)
def get_salon(salon_id: int, db: Session = Depends(get_db)):
    salon = salon_service.get_salon(db, salon_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return salon


# POST
@router.post("/", response_model=SalonResponse, status_code=201)
def create_salon(
    salon_data: SalonCreate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    return salon_service.create_salon(db, salon_data)


# PATCH
@router.patch("/{salon_id}", response_model=SalonResponse)
def update_salon(
    salon_id: int,
    salon_data: SalonUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    salon = salon_service.get_salon(db, salon_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return salon_service.update_salon(db, salon_id, salon_data)


# DELETE
@router.delete("/{salon_id}")
def delete_salon(
    salon_id: int, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    salon = salon_service.get_salon(db, salon_id)
    
    if salon is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    salon_service.delete_salon(db, salon_id)
    
    return {"message": "Salon deleted successfully"}