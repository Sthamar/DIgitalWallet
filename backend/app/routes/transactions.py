from fastapi import APIRouter, HTTPException, Depends, status
from models.transaction import Transaction
from schemas.transaction import TransactionOut
from models.wallet import Wallet
from models.expense import Expense
from schemas.moneyTransfer import MoneyTransferRequest, MoneyTransferResponse
from database import get_db
from oauth2 import get_current_user
from sqlalchemy.orm import Session
from typing import List
from core.security import role_required
from typing import List
from core.services import transfer_money
from core.security import verify_password


router = APIRouter(prefix="/transactions", tags=["transactions"])


@router.get("/admin", response_model=List[TransactionOut])
def get_all_users_transactions(current_user:str = Depends(role_required(["admin","auditor"])), db:Session = Depends(get_db)):
    transactions = db.query(Transaction).all()
    if not transactions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    return transactions

@router.get('/transactions/debit-credit', response_model=List[TransactionOut])
def get_debit_credit_transaction(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    transactions = db.query(Transaction).filter(Transaction.transaction_type.in_(['credit','debit']), Transaction.user_id == current_user.id).all()
    if transactions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    return transactions


@router.get('/transactions/send', response_model=List[TransactionOut])
def get_send_transaction(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wallet not found")
    
    transactions = db.query(Transaction).filter(Transaction.transaction_type == 'send', wallet.id == Transaction.sender_wallet_id).all()
    if transactions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    return transactions

@router.get('/transactions/received', response_model=List[TransactionOut])
def get_received_transaction(db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User wallet not found")
    
    transactions = db.query(Transaction).filter(Transaction.transaction_type == 'receive', Transaction.receiver_wallet_id == wallet.id).all()
    if transactions is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    return transactions



@router.delete("/admin/{transaction_id}")
def delete_transaction(transaction_id:int, current_user:str = Depends(role_required(["admin"])), db:Session = Depends(get_db)):
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    if not transaction:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No transactions found")
    db.delete(transaction)
    db.commit()
    return {"data":transaction, "message": "deleted successfully"}


@router.post("/send-money", response_model=MoneyTransferResponse)
def send_money(
    transfer_request: MoneyTransferRequest,
    current_user= Depends(get_current_user),
    db: Session = Depends(get_db)
):
    
    if not verify_password(transfer_request.pin, current_user.pin):
        raise HTTPException(status_code=403, detail="Invalid PIN")
    
    
    sender_wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not sender_wallet:
        raise HTTPException(status_code=404, detail="Sender's wallet not found")
    
    sender_wallet, receiver_wallet = transfer_money(
        db=db,
        sender_id=current_user.id,
        receiver_wallet_id=transfer_request.receiver_wallet_id,
        amount=transfer_request.amount,
        category_id=transfer_request.category_id,
        description=transfer_request.description
    )
    
    return MoneyTransferResponse(
        message="Money transferred successfully",
        sender_balance=sender_wallet.balance
    )
