from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ReservationCreate(BaseModel):
    customer_id: int = Field(gt=0)
    staff_id: int = Field(gt=0)
    menu_id: int = Field(gt=0)
    start_at: datetime
    
    
class ReservationUpdate(BaseModel):
    start_at: datetime | None = None
    
    
class ReservationResponse(BaseModel):
    id: int
    customer_id: int
    staff_id: int
    menu_id: int
    start_at: datetime
    end_at: datetime
    
    model_config = ConfigDict(from_attributes=True)