from database import Base
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    transaction_id = Column(String(255), nullable=False, unique=True)
    token = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), nullable=False)
    payment_method = Column(String(50), nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())
    user = relationship("User", back_populates="payments")