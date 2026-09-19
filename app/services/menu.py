from sqlalchemy.orm import Session

from app.models.menu import Menu
from app.models.salon import Salon
from app.schemas.menu import MenuCreate, MenuUpdate


# GET
def get_menus(db: Session):
    return db.query(Menu).all()


# GET_ID
def get_menu(db: Session, menu_id: int):
    return db.get(Menu, menu_id)


# POST
def create_menu(db: Session, menu_data: MenuCreate):
    salon = db.get(Salon, menu_data.salon_id)
    
    if salon is None:
        return None
    
    new_menu = Menu(
        name=menu_data.name,
        price=menu_data.price,
        duration_minutes=menu_data.duration_minutes,
        salon_id=menu_data.salon_id
    )
    
    db.add(new_menu)
    db.commit()
    db.refresh(new_menu)
    
    return new_menu


# PATCH
def update_menu(
    db: Session,
    menu_id: int,
    menu_data: MenuUpdate
):
    menu = db.get(Menu, menu_id)
    
    if menu is None:
        return None
    
    update_data = menu_data.model_dump(exclude_unset=True)
    
    if "salon_id" in update_data:
        salon = db.get(Salon, update_data["salon_id"])
        
        if salon is None:
            return None
        
    for key, value in update_data.items():
        setattr(menu, key, value)
        
    db.commit()
    db.refresh(menu)
    
    return menu


# DELETE
def delete_menu(db: Session, menu_id: int):
    menu = db.get(Menu, menu_id)
    
    if menu is None:
        return None
    
    db.delete(menu)
    db.commit()
    
    return menu