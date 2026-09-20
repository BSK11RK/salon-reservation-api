from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.customer import CustomerResponse
from app.schemas.menu import MenuResponse
from app.schemas.staff import StaffResponse


class ReservationCreate(BaseModel):
    customer_id: int = Field(gt=0)
    staff_id: int = Field(gt=0)
    menu_id: int = Field(gt=0)
    start_at: datetime
    
    
class ReservationUpdate(BaseModel):
    start_at: datetime | None = None
    
    
class ReservationResponse(BaseModel):
    id: int
    customer: CustomerResponse
    staff: StaffResponse
    menu: MenuResponse
    start_at: datetime
    end_at: datetime
    
    model_config = ConfigDict(from_attributes=True)