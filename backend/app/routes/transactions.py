from fastapi import APIRouter, HTTPException, Depends, status
from models.transaction import Transaction
from schemas.transaction import TransactionOut
from database import get_db
from oauth2 import get_current_user
from sqlalchemy.orm import Session
from typing import List
from core.security import role_required
from typing import List


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/admin", response_model=List[TransactionOut])
def get_all_users_transactions(current_user:str = Depends(role_required(["admin","auditor"])), db:Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    return transactions

@router.get("/transactions", response_model=List[TransactionOut])
def get_transactoins(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    transactions = db.query(Transaction).filter(Transaction.user_id == current_user.id).all()
    if not transactions:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    return transactions

@router.delete("/admin/{transaction_id}")
def delete_transaction(transaction_id:int, current_user:str = Depends(role_required(["admin"])), db:Session = Depends(get_db)):
    transaction = transactions = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    db.delete(transaction)
    db.commit()
    return {"data":transaction, "message": "deleted successfully"}