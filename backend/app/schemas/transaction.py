from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TransactionOut(BaseModel):
    id: int
    amount: float
    description: Optional[str]
    transaction_type: str
    transaction_date: Optional[datetime]
    
    
    class Config:
        from_attributes = True
