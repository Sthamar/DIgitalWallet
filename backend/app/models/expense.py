from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship



class Expense(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    category_id = Column(Integer, ForeignKey("budget_categories.id", ondelete="SET NULL"))
    description = Column(String(255), nullable=False)
    amount = Column(Numeric(10, 2), nullable=False)
    expense_date = Column(TIMESTAMP, server_default=func.now())
    created_at = Column(TIMESTAMP, server_default=func.now())
    
    user = relationship("User", back_populates="expenses")