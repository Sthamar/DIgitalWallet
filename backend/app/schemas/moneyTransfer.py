from pydantic import BaseModel, condecimal
from typing import Optional

class MoneyTransferRequest(BaseModel):
    receiver_wallet_id: int
    amount: condecimal(max_digits=10, decimal_places=2)
    category_id: int
    description: str
    

class MoneyTransferResponse(BaseModel):
    message: str
    sender_balance: condecimal(max_digits=10, decimal_places=2)
    
    
    