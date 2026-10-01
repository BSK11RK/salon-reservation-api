from fastapi import FastAPI

from app.routers.salons import router as salon_router
from app.routers.staffs import router as staff_router
from app.routers.menus import router as menu_router
from app.routers.customers import router as customer_router
from app.routers.reservations import router as reservation_router
from app.routers.users import router as user_router
from app.routers.auth import router as auth_router


app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(salon_router)
app.include_router(menu_router)
app.include_router(staff_router)
app.include_router(customer_router)
app.include_router(reservation_router)