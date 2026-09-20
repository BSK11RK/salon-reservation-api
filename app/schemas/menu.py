from pydantic import BaseModel, ConfigDict, Field


class MenuCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    price: int = Field(ge=0)
    duration_minutes: int = Field(gt=0)
    salon_id: int = Field(gt=0)
    
    
class MenuUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    price: int | None = Field(default=None, ge=0)
    duration_minutes: int | None = Field(default=None, gt=0)
    salon_id: int | None = Field(default=None, gt=0)
    
    
class MenuResponse(BaseModel):
    id: int
    name: str
    price: int
    duration_minutes: int
    salon_id: int

    model_config = ConfigDict(from_attributes=True)