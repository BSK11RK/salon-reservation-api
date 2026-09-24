from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import get_current_user
from app.schemas.customer import (
    CustomerCreate, 
    CustomerUpdate, 
    CustomerResponse
)
from app.services import customer as customer_service


router = APIRouter(prefix="/customers", tags=["customers"])


# GET
@router.get("/", response_model=list[CustomerResponse])
def get_customers(db: Session = Depends(get_db)):
    return customer_service.get_customers(db)


# GET_ME
@router.get("/me", response_model=CustomerResponse)
def get_my_customer(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    customer = customer_service.get_customer_by_user_id(db, current_user.id)
    
    if customer is None:
        raise HTTPException(
            status_code=404, 
            detail="Customer profile not found"
        )
    
    return customer


# GET_ID
@router.get("/{customer_id}", response_model=CustomerResponse)
def get_customer(customer_id: int, db: Session= Depends(get_db)):
    customer = customer_service.get_customer(db, customer_id)
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer


# POST
@router.post("/", response_model=CustomerResponse, status_code=201)
def create_customer(
    customer_data: CustomerCreate, 
    db: Session = Depends(get_db)
):
    customer = customer_service.create_customer(db, customer_data)
    
    if customer is "user_not_found":
        raise HTTPException(status_code=404, detail="User not found")
    
    if customer == "customer_exists":
        raise HTTPException(status_code=409, detail="Customer already exists")
    
    return customer


# PATCH
@router.patch("/{customer_id}", response_model=CustomerResponse)
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
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return customer
        

# DELETE
@router.delete("/{customer_id}")
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = customer_service.delete_customer(db, customer_id)
    
    if customer is None:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    return {"message": "Customer deleted successfully"}