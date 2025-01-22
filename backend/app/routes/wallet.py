from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.wallet import Wallet
from models.transaction import Transaction
from database import get_db
from oauth2 import get_current_user
from schemas.wallet import WalletAddFunds, WalletOut
from core.security import role_required
from typing import List


router = APIRouter(prefix="/wallet", tags=["Wallet"])



def get_or_create_wallet(current_user, db:Session):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id = current_user.id)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


@router.get("/admin", response_model=List[WalletOut])
def get_all_users_wallet(current_user: str = Depends(role_required(["admin"])), db: Session = Depends(get_db)):
    wallets = db.query(Wallet).all()
    if not wallets:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail="No wallet found")
    return wallets

@router.get("/", response_model=WalletOut)
def get_wallet_balance(current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    wallet = get_or_create_wallet(current_user, db)
    return wallet


@router.post("/add-funds", response_model=WalletOut)
def add_funds(data: WalletAddFunds, current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    wallet = get_or_create_wallet(current_user, db)
    if data.amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Amount must be greater than zero")
    
    wallet.balance += data.amount
    db.commit()
    db.refresh(wallet)
    
    new_transaction = Transaction(
        user_id = current_user.id,
        transaction_type = "credit",
        amount = data.amount,
        description = f"Added {data.amount} to wallet"
    )
    db.add(new_transaction)
    db.commit()
    
    return wallet

@router.delete("/admin/{wallet_id}")
def delete_users_wallet(wallet_id: int, current_user:str = Depends(role_required(["admin"])), db:Session = Depends(get_db)):
    wallet = db.query(Wallet).filter(Wallet.id == wallet_id).first()
    if not wallet:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No wallet found")
    db.delete(wallet)
    db.commit()
    return {"data":wallet, "message": "deleted successfully"}