from pydantic import BaseModel


class SalonCreate(BaseModel):
    name: str
    address: str


class SalonUpdate(BaseModel):
    name: str | None = None
    address: str | None = None