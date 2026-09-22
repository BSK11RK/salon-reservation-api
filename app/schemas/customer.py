from pydantic import BaseModel, Field


class CustomerCreate(BaseModel):
    user_id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    
    
class CustomerUpdate(BaseModel):
    name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100
    )
    

class CustomerResponse(BaseModel):
    id: int
    user_id: int
    name: str

    model_config = {"from_attributes=True": True}