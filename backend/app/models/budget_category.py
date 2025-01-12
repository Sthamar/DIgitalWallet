from database import Base
from sqlalchemy import Column, Integer, String, TIMESTAMP, Numeric, ForeignKey,Boolean
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from decimal import Decimal


class BudgetCategory(Base):
    __tablename__ = "budget_categories"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), index=True)
    name = Column(String(100), unique=True, nullable=False)
    monthly_limit = Column(Numeric(10, 2), nullable=False)
    over_spend = Column(Boolean, default=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    user = relationship("User", back_populates="budget_categories")
    
    
    # Add a calculated property for the remaining budget
    @property
    def remaining_budget(self):
        total_expenses = sum(expense.amount for expense in self.user.expenses if expense.category_id == self.id)
        return Decimal(self.monthly_limit) - total_expenses