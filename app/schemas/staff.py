from pydantic import BaseModel, ConfigDict, Field


class StaffCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    salon_id: int = Field(gt=0)
    
    
class StaffUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    salon_id: int | None = Field(default=None, gt=0)
    
    
class StaffResponse(BaseModel):
    id: int
    name: str
    salon_id: int
    
    model_config = ConfigDict(from_attributes=True)