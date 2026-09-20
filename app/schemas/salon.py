from pydantic import BaseModel, ConfigDict


class SalonCreate(BaseModel):
    name: str
    address: str


class SalonUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    
    
class SalonResponse(BaseModel):
    id: int
    name: str
    address: str
    
    model_config = ConfigDict(from_attributes=True)