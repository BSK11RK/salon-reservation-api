from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.security import require_admin
from app.schemas.menu import MenuCreate, MenuUpdate, MenuResponse
from app.services import menu as menu_service


router = APIRouter(prefix="/menus", tags=["menus"])


# GET
@router.get("/", response_model=list[MenuResponse])
def get_menus(db: Session = Depends(get_db)):
    return menu_service.get_menus(db)


# GET_ID
@router.get("/{menu_id}", response_model=MenuResponse)
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = menu_service.get_menu(db, menu_id)
    
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    return menu


# POST
@router.post("/", response_model=MenuResponse, status_code=201)
def create_menu(
    menu_data: MenuCreate, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    menu = menu_service.create_menu(db, menu_data)
    
    if menu == "salon_not_found":
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return menu


# PATCH
@router.patch("/{menu_id}", response_model=MenuResponse)
def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    menu = menu_service.get_menu(db, menu_id)

    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")

    menu = menu_service.update_menu(db, menu_id, menu_data)

    if menu == "salon_not_found":
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return menu


# DELETE
@router.delete("/{menu_id}")
def delete_menu(
    menu_id: int, 
    current_user: User = Depends(require_admin),
    db: Session = Depends(get_db)
):
    menu = menu_service.get_menu(db, menu_id)
    
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    menu_service.delete_menu(db, menu_id)
    
    return {"message": "Menu deleted successfully"}