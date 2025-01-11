from pydantic import BaseModel, condecimal
from typing import Optional
from datetime import datetime

class ExpenseBase(BaseModel):
    description: str
    amount: condecimal(max_digits=10, decimal_places=2)
    category_id: Optional[int]
    expense_date: Optional[datetime]
    
    
class ExpenseCreate(ExpenseBase):
    """Schema for creating a new expense"""
    pass

class ExpenseUpdate(BaseModel):
    """Schema for updating an existing expense"""
    description: Optional[str]
    amount: Optional[condecimal(max_digits=10, decimal_places=2)]
    category_id: Optional[int]
    expense_date: Optional[datetime]
    

class ExpenseOut(ExpenseBase):
    """Schema for returning expense details"""
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True