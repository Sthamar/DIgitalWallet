from database import Base
from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index= True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False )
    password_hash = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    wallet = relationship("Wallet", back_populates="user", uselist=False)
    budget_categories = relationship("BudgetCategory", back_populates="user")
    expenses = relationship("Expense", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
