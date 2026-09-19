from datetime import timedelta

from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.menu import Menu
from app.models.reservation import Reservation
from app.models.staff import Staff
from app.schemas.reservation import ReservationCreate


# POST
def create_reservation(db: Session, reservation_data: ReservationCreate):
    customer = db.get(Customer, reservation_data.customer_id)
    
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
        customer_id=reservation_data.customer_id,
        staff_id=reservation_data.staff_id,
        menu_id=reservation_data.menu_id,
        start_at=reservation_data.start_at,
        end_at=end_at
    )
    
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)
    
    return new_reservation