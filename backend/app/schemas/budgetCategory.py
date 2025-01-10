from pydantic import BaseModel, Field, field_validator
from typing import Optional
from datetime import datetime

class BudgetCategoryCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Name of the budget category")
    monthly_limit: float = Field(..., gt= 0, description="Monthly spending limit for the category")
    
    @field_validator("name")
    def no_special_characters(cls, value):
        if not value.isalnum():
            raise ValueError("Category name must only contain letters and numbers")
        return value
    

class BudgetCategoryOut(BaseModel):
    id: int
    name: str
    monthly_limit: float
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda dt: dt.isoformat(), 
        }
        
class BudgetCategoryUpdate(BaseModel):
    name:str
    monthly_limit: float
        
