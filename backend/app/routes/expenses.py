from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from typing import List
from models.expense import Expense
from models.budget_category import BudgetCategory
from schemas.expenses import ExpenseCreate, ExpenseOut,ExpenseUpdate
from database import get_db
from oauth2 import get_current_user

router = APIRouter(prefix="/expenses", tags=['Expenses'])

@router.post("/", response_model=ExpenseOut)
def create_expense(expense: ExpenseCreate, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    if expense.category_id:
        category = db.query(BudgetCategory).filter(BudgetCategory.id == expense.category_id, BudgetCategory.user_id == current_user.id).first()
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    
        new_expense = Expense(
            user_id = current_user.id,
            category_id = expense.category_id,
            description = expense.description,
            amount = expense.amount,
            expense_date = expense.expense_date or func.now(),
        )
    
    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)
    return new_expense


@router.get("/", response_model=List[ExpenseOut])
def get_all_expenses(
    start_date: str = None,
    end_date: str = None,
    category_id: int = None,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    q = db.query(Expense).filter(Expense.user_id == current_user.id)
    
    
    if start_date:
        q = q.filter(Expense.expense_date >= start_date)
    if end_date:
        q = q.filter(Expense.expense_date <= end_date)
    if category_id:
        q = q.filter(Expense.category_id == category_id)
        
    expenses = q.all()
    return expenses



@router.put("/{expense_id}", response_model=ExpenseOut)
def update_expense(expense_id: int, expense_update: ExpenseUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    
    if expense_update.description:
        expense.description = expense_update.description
    if expense_update.amount:
        expense.amount = expense_update.amount
    if expense_update.category_id:
        category = db.query(BudgetCategory).filter(
            BudgetCategory.id == expense_update.category_id,
            BudgetCategory.user_id == current_user.id
        ).first()
        
        if not category:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
        expense.category_id = expense_update.category_id
    if expense_update.expense_date:
        expense.expense_date = expense_update.expense_date
        
    db.commit()
    db.refresh(expense)
    return expense





@router.delete("/{expense_id}")
def delete_expense(expense_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    expense = db.query(Expense).filter(
        Expense.id == expense_id,
        Expense.user_id == current_user.id
    ).first()
    if not expense:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Expense not found")
    db.delete(expense)
    db.commit()
    return {"message": "Expense deleted successfully"}