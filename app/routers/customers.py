from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.customer import CustomerCreate, CustomerUpdate
from app.services import customer as customer_service


router = APIRouter(prefix="/customers", tags=["customers"])


# GET
@router.get("/")
def get_customers(db: Session = Depends(get_db)):
    return customer_service.get_customers(db)


# GET_ID
@router.get("/{customer_id}")
def get_customer(customer_id: int, db: Session= Depends(get_db)):
    customer = customer_service.get_customer(db, customer_id)
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer


# POST
@router.post("/")
def create_customer(
    customer_data: CustomerCreate, 
    db: Session = Depends(get_db)
):
    customer = customer_service.create_customer(db, customer_data)
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Email already exists")
    
    return customer


# PATCH
@router.patch("/{customer_id}")
def update_customer(
    customer_id: int,
    customer_data: CustomerUpdate,
    db: Session = Depends(get_db)
):
    customer = customer_service.update_customer(
        db, 
        customer_id, 
        customer_data
    )
    
    if customer is None:
        raise HTTPException(
            status_code=404,
            detail="Customer not found or email already exists"
        )
        

# DELETE
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = customer_service.delete_customer(db, customer_id)
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": "Customer deleted successfully"}