from database import Base
from sqlalchemy import Column, Integer, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Wallet(Base):
    __tablename__ = "wallets"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    balance = Column(Numeric(10, 2), default=0.00)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="wallet")
    sent_transactions = relationship("Transaction", back_populates = "sender_wallet", foreign_keys="[Transaction.sender_wallet_id]")
    received_transactions = relationship("Transaction", back_populates="receiver_wallet", foreign_keys="[Transaction.receiver_wallet_id]")
    