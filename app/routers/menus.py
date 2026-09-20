from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.menu import MenuCreate, MenuUpdate
from app.services import menu as menu_service


router = APIRouter(prefix="/menus", tags=["menus"])


# GET
@router.get("/")
def get_menus(db: Session = Depends(get_db)):
    return menu_service.get_menus(db)


# GET_ID
@router.get("/{menu_id}")
def get_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = menu_service.get_menu(db, menu_id)
    
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    return menu


# POST
@router.post("/")
def create_menu(menu_data: MenuCreate, db: Session = Depends(get_db)):
    menu = menu_service.create_menu(db, menu_data)
    
    if menu is None:
        raise HTTPException(status_code=404, detail="Salon not found")
    
    return menu


# PATCH
@router.patch("/{menu_id}")
def update_menu(
    menu_id: int,
    menu_data: MenuUpdate,
    db: Session = Depends(get_db)
):
    menu = menu_service.update_menu(db, menu_id, menu_data)
    
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu or Salon not found")
    
    return menu


# DELETE
@router.delete("/{menu_id}")
def delete_menu(menu_id: int, db: Session = Depends(get_db)):
    menu = menu_service.delete_menu(db, menu_id)
    
    if menu is None:
        raise HTTPException(status_code=404, detail="Menu not found")
    
    return {"message": "Menu deleted successfully"}