from sqlalchemy.orm import Session

from app.models.customer import Customer
from app.models.user import User
from app.schemas.customer import CustomerCreate, CustomerUpdate


# GET
def get_customers(db: Session):
    return db.query(Customer).all()


# GET_ID
def get_customer(db: Session, customer_id: int):
    return db.get(Customer, customer_id)


# POST
def create_customer(db: Session, customer_data: CustomerCreate):
    user = db.get(User, customer_data.user_id)
    
    if user is None:
        return "user_not_found"
    
    existing_customer = db.query(Customer).filter(
        Customer.user_id == customer_data.user_id
    ).first()
    
    if existing_customer is not None:
        return "customer_exists"
    
    new_customer = Customer(
        user_id=customer_data.user_id,
        name=customer_data.name
    )
    
    db.add(new_customer)
    db.commit()
    db.refresh(new_customer)
    
    return new_customer


# PATCH
def update_customer(
    db: Session,
    customer_id: int,
    customer_data: CustomerUpdate
):
    customer = db.get(Customer, customer_id)
    
    if customer is None:
        return None
    
    update_data = customer_data.model_dump(exclude_unset=True)
        
    for key, value in update_data.items():
        setattr(customer, key, value)
        
    db.commit()
    db.refresh(customer)
    
    return customer


# DELETE
def delete_customer(db: Session, customer_id: int):
    customer = db.get(Customer, customer_id)
    
    if customer is None:
        return None
    
    db.delete(customer)
    db.commit()
    
    return customer