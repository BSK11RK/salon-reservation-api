from datetime import datetime

from pydantic import BaseModel, Field


class ReservationCreate(BaseModel):
    customer_id: int = Field(gt=0)
    staff_id: int = Field(gt=0)
    menu_id: int = Field(gt=0)
    start_at: datetime
    
    
class ReservationUpdate(BaseModel):
    start_at: datetime | None = None