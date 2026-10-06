from fastapi import FastAPI

from fastapi import FastAPI

from app.routers import (
    auth,
    customers,
    menus,
    reservations,
    salons,
    staffs,
    users
)


app = FastAPI(title="Beauty Salon Reservation API")

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(salons.router)
app.include_router(staffs.router)
app.include_router(menus.router)
app.include_router(customers.router)
app.include_router(reservations.router)