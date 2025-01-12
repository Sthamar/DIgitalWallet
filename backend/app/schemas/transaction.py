from pydantic import BaseModel
from datetime import datetime


class TransactionOut(BaseModel):
    id: int
    transaction_type: str
    transaction_date: datetime
    description: str
    
    class Config:
        from_attributes = True
