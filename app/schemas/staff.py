from pydantic import BaseModel


class StaffCreate(BaseModel):
    name: str
    salon_id: int
    
    
class StaffUpdate(BaseModel):
    name: str | None = None
    salon_id: int | None = None