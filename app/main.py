from fastapi import FastAPI

from app.database import Base, engine
from app.models.salon import Salon
from app.routers.salons import router as salom_router


Base.metadata.create_all(bind=engine)


app = FastAPI()

app.include_router(salom_router)