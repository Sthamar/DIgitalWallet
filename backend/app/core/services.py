from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.wallet import Wallet
from models.transaction import Transaction
from models.expense import Expense

def transfer_money(db: Session, sender_id: int, receiver_wallet_id: int, amount: float, category_id: int = None, description: str = None):
    # Fetch sender and receiver wallets
    receiver_wallet = db.query(Wallet).filter(Wallet.id == receiver_wallet_id).first()
    sender_wallet = db.query(Wallet).filter(Wallet.user_id == sender_id).first()

    if not receiver_wallet:
        raise HTTPException(status_code=404, detail="Receiver wallet not found")
    if not sender_wallet:
        raise HTTPException(status_code=404, detail="Sender wallet not found")
    if sender_wallet.balance < amount:
        raise HTTPException(status_code=400, detail="Insufficient balance in sender's account")
    if sender_wallet.id == receiver_wallet.id:
        raise HTTPException(status_code=400, detail="Cannot send money to the same account")

    # Update balances
    sender_wallet.balance -= amount
    receiver_wallet.balance += amount

    # Log sender's transaction
    sender_transaction = Transaction(
        user_id = sender_id,
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=amount,
        transaction_type="send",
        description=f"Sent money to wallet ID {receiver_wallet.id}"
    )
    db.add(sender_transaction)

    # Log receiver's transaction
    receiver_transaction = Transaction(
        user_id = receiver_wallet.user_id,
        sender_wallet_id=sender_wallet.id,
        receiver_wallet_id=receiver_wallet.id,
        amount=amount,
        transaction_type="receive",
        description=f"Received money from wallet ID {sender_wallet.id}"
    )
    db.add(receiver_transaction)

    # Log expense if category_id is provided
    if category_id:
        expense = Expense(
            user_id=sender_wallet.user_id,
            category_id=category_id,
            description=description or f"Transfer to Wallet ID {receiver_wallet.id}",
            amount=amount
        )
        db.add(expense)

    db.commit()
    db.refresh(sender_wallet)
    db.refresh(receiver_wallet)

    return sender_wallet, receiver_wallet