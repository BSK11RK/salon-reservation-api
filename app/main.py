from fastapi import FastAPI

from app.database import Base, engine

from app.models.salon import Salon
from app.models.staff import Staff
from app.models.menu import Menu
from app.models.customer import Customer
from app.models.reservation import Reservation

from app.routers.salons import router as salom_router
from app.routers.staffs import router as staff_router
from app.routers.menus import router as menu_router
from app.routers.customers import router as customer_router


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(salom_router)
app.include_router(staff_router)
app.include_router(menu_router)
app.include_router(customer_router)