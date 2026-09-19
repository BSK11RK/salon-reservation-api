from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.schemas.reservation import ReservationCreate
from app.services import reservation as reservation_service


router = APIRouter(prefix="/reservations", tags=["reservations"])


# POST
@router.post("/")
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