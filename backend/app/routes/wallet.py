from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.wallet import Wallet
from database import get_db
from oauth2 import get_current_user
from schemas.wallet import WalletAddFunds, WalletOut

router = APIRouter(prefix="/wallet", tags=["Wallet"])

def get_or_create_wallet(current_user, db:Session):
    wallet = db.query(Wallet).filter(Wallet.user_id == current_user.id).first()
    if not wallet:
        wallet = Wallet(user_id = current_user.id)
        db.add(wallet)
        db.commit()
        db.refresh(wallet)
    return wallet


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
    return wallet