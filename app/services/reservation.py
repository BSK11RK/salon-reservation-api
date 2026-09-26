from datetime import timedelta

from sqlalchemy.orm import Session, joinedload

from app.models.customer import Customer
from app.models.menu import Menu
from app.models.reservation import Reservation
from app.models.staff import Staff
from app.schemas.reservation import ReservationCreate, ReservationUpdate


# GET
def get_reservations(db: Session):
    return (
    db.query(Reservation)
    .options(
        joinedload(Reservation.customer),
        joinedload(Reservation.staff),
        joinedload(Reservation.menu),
    )
    .all()
)


# GET_ID
def get_reservation(db: Session, reservation_id: int):
    return (
        db.query(Reservation)
        .options(
            joinedload(Reservation.customer),
            joinedload(Reservation.staff),
            joinedload(Reservation.menu),
        )
        .filter(Reservation.id == reservation_id)
        .first()
    )


# POST
def create_reservation(
    db: Session, 
    customer_id: int,
    reservation_data: ReservationCreate
):
    customer = db.get(Customer, customer_id)
    
    if customer is None:
        return "customer_not_found"
    
    staff = db.get(Staff, reservation_data.staff_id)
    
    if staff is None:
        return "staff_not_found"
    
    menu = db.get(Menu, reservation_data.menu_id)
    
    if menu is None:
        return "menu_not_found"
    
    end_at = reservation_data.start_at + timedelta(
        minutes=menu.duration_minutes
    )
    
    overlapping_reservation = db.query(Reservation).filter(
        Reservation.staff_id
        == reservation_data.staff_id,
        Reservation.start_at < end_at,
        Reservation.end_at
        > reservation_data.start_at
    ).first()
    
    if overlapping_reservation is not None:
        return "time_conflict"
    
    new_reservation = Reservation(
        customer_id=customer_id,
        staff_id=reservation_data.staff_id,
        menu_id=reservation_data.menu_id,
        start_at=reservation_data.start_at,
        end_at=end_at
    )
    
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    return new_reservation


# PATCH
def update_reservation(
    db: Session,
    reservation_id: int,
    reservation_data: ReservationUpdate
):
    reservation = db.get(Reservation, reservation_id)
    
    if reservation is None:
        return "reservation_not_found"
    
    update_data = reservation_data.model_dump(exclude_unset=True)
    
    if "start_at" in update_data:
        new_start_at = update_data["start_at"]
        
        menu = db.get(Menu, reservation.menu_id)
        
        if menu is None:
            return "menu_not_found"
        
        new_end_at = new_start_at + timedelta(minutes=menu.duration_minutes)
        
        overlapping_reservation = db.query(Reservation).filter(
            Reservation.staff_id == reservation.staff_id,
            Reservation.id != reservation.id,
            Reservation.start_at < new_end_at,
            Reservation.end_at > new_start_at
        ).first()
        
        if overlapping_reservation is not None:
            return "time_conflict"
        
        reservation.start_at = new_start_at
        reservation.end_at = new_end_at
        
    db.commit()
    db.refresh(reservation)
    
    return reservation


# DELETE
def delete_reservation(db: Session, reservation_id: int):
    reservation = db.get(Reservation, reservation_id)
    
    if reservation is None:
        return None
    
    db.delete(reservation)
    db.commit()
    
    return reservation