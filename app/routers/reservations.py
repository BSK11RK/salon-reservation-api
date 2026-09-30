from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import (
    get_current_user, 
    require_customer, 
    require_staff, 
    require_admin
)
from app.schemas.reservation import (
    ReservationCreate, 
    ReservationUpdate,
    ReservationResponse
)
from app.services import reservation as reservation_service
from app.services.customer import get_customer_by_user_id
from app.services.staff import get_staff_by_user_id


router = APIRouter(prefix="/reservations", tags=["reservations"])


# GET
@router.get("/", response_model=list[ReservationResponse])
def get_reservations(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "admin":
        return reservation_service.get_reservations(db)
    
    if current_user.role == "customer":
        customer = get_customer_by_user_id(db, current_user.id)
    
        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer profile not found"
            )
    
        return reservation_service.get_reservations_by_customer(
            db,
            customer.id
        )
        
    if current_user.role == "staff":
        staff = get_staff_by_user_id(db, current_user.id)
        
        if staff is None:
            raise HTTPException(
                status_code=404,
                detail="Staff profile not found"
            )

        return reservation_service.get_reservations_by_staff(db, staff.id)
    
    raise HTTPException(status_code=403, detail="Invalid role")


# STAFF_ME
@router.get("/staff/me", response_model=list[ReservationResponse])
def get_my_staff_reservations(
    current_user: User = Depends(require_staff),
    db: Session = Depends(get_db)
):
    staff = get_staff_by_user_id(db, current_user.id)
    
    if staff is None:
        raise HTTPException(
            status_code=404,
            detail="Staff profile not found"
        )
        
    return reservation_service.get_reservations_by_staff(db, staff.id)


# GET_ID
@router.get("/{reservation_id}", response_model=ReservationResponse)
def get_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "admin":
        reservation = reservation_service.get_reservation(
            db, 
            reservation_id
        )
        
        if reservation is None:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )
            
        return reservation
    
    if current_user.role == "customer":
        customer = get_customer_by_user_id(db, current_user.id)
        
        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer profile not found"
            )
            
        reservation = reservation_service.get_reservation_by_customer(
            db,
            reservation_id,
            customer.id
        )
        
        if reservation is None:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )
            
        return reservation
    
    if current_user.role == "staff":
        staff = get_staff_by_user_id(db, current_user.id)
        
        if staff is None:
            raise HTTPException(
                status_code=404,
                detail="Staff profile not found"
            )
            
        reservation = reservation_service.get_reservation_by_staff(
            db, reservation_id,
            staff.id
        )
        
        if reservation is None:
            raise HTTPException(
                status_code=404,
                detail="Reservation not found"
            )
            
        return reservation
    
    raise HTTPException(status_code=403, detail="Invalid role")


# POST
@router.post("/", response_model=ReservationResponse)
def create_reservation(
    reservation_data: ReservationCreate, 
    current_user: User = Depends(require_customer),
    db: Session = Depends(get_db)
):
    customer = get_customer_by_user_id(db, current_user.id)

    if customer is None:
        raise HTTPException(
            status_code=404, 
            detail="Customer profile not found"
        )
    
    reservation = reservation_service.create_reservation(
        db, 
        customer.id,
        reservation_data
    )

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
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "admin":
        reservation = reservation_service.update_reservation(
            db,
            reservation_id,
            reservation_data
        )
        
    elif current_user.role == "customer":
        customer = get_customer_by_user_id(db, current_user.id)
    
        if customer is None:
            raise HTTPException(
                status_code=404, 
                detail="Customer profile not found"
            )
    
        reservation = reservation_service.update_reservation(
            db,
            reservation_id,
            reservation_data,
            customer.id
        )
    
    else:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to update this reservation"
        )
    
    if reservation == "reservation_not_found":
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    if reservation == "menu_not_found":
        raise HTTPException(status_code=404, detail="Menu not found")
    
    if reservation == "time_conflict":
        raise HTTPException(
            status_code=409,
            detail="Staff is already reserved at this time"
        )
        
    return reservation


# DELETE
@router.delete("/{reservation_id}")
def delete_reservation(
    reservation_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if current_user.role == "admin":
        reservation = reservation_service.delete_reservation(
            db,
            reservation_id
        )

    elif current_user.role == "customer":
        customer = get_customer_by_user_id(db, current_user.id)

        if customer is None:
            raise HTTPException(
                status_code=404,
                detail="Customer profile not found"
            )
            
        reservation = reservation_service.delete_reservation(
            db,
            reservation_id,
            customer.id
        )
        
    else:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this reservation"
        )
    
    if reservation is None:
        raise HTTPException(status_code=404, detail="Reservation not found")
    
    return {"message": "Reservation deleted successfully"}