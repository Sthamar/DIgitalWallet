from pydantic import BaseModel
from decimal import Decimal

class WalletAddFunds(BaseModel):
    amount: Decimal

class WalletOut(BaseModel):
    id:int
    balance: Decimal
    
    class Config:
        from_attributes = True