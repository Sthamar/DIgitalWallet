from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship




class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    sender_wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"))
    receiver_wallet_id = Column(Integer, ForeignKey("wallets.id", ondelete="CASCADE"))
    transaction_type = Column(String(50), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_date = Column(TIMESTAMP, server_default=func.now())
    description = Column(String(255))
    
    sender_wallet = relationship("Wallet", foreign_keys=[sender_wallet_id], back_populates="sent_transactions")
    receiver_wallet = relationship("Wallet", foreign_keys=[receiver_wallet_id], back_populates="received_transactions")