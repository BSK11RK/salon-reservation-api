from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.schemas.reservation import (
    ReservationCreate, 
    ReservationUpdate,
    ReservationResponse
)
from app.services import reservation as reservation_service


router = APIRouter(prefix="/reservations", tags=["reservations"])


# GET
@router.get("/", response_model=list[ReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return reservation_service.get_reservations(db)


# GET_ID
@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    reservation = reservation_service.get_reservations(db, reservation_id)
    
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    return reservation


# POST
@router.post("/", response_model=ReservationResponse)
def create_reservation(
    reservation_data: ReservationCreate, 
    db: Session = Depends(get_db)
):
    reservation = reservation_service.create_reservation(
        db, 
        reservation_data
    )

    if reservation == "customer_not_found":
        raise HTTPException(status_code=404, detail="Customer not found")

    if reservation == "staff_not_found":
        raise HTTPException(status_code=404, detail="Staff not found")

    if reservation == "menu_not_found":
        raise HTTPException(status_code=404, detail="Menu not found")

    if reservation == "time_conflict":
        raise HTTPException(
            status_code=409,
            detail="Staff is already reserved at this time"
        )

    return reservation


# PATCH
@router.patch("/{reservation_id}", response_model=ReservationResponse)
def update_reservation(
    reservation_id: int,
    reservation_data: ReservationUpdate,
    db: Session = Depends(get_db)
):
    reservation = reservation_service.update_reservation(
        db,
        reservation_id,
        reservation_data
    )
    
    if reservation == "reservation_not_found":
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    if reservation == "menu_not_found":
        raise HTTPException(status_code=404, detail="Menu not found")
    
    if reservation == "time_conflict":
        raise HTTPException(
            status_code=404,
            detail="Staff is already reserved at this time"
        )
        
    return reservation


# DELETE
@router.delete("/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    db: Session = Depends(get_db)
):
    reservation = reservation_service.delete_reservation(
        db,
        reservation_id
    )
    
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    return {"message": "Reservation deleted successfully"}