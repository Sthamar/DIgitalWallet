from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.budget_category import BudgetCategory
from schemas.budgetCategory import BudgetCategoryCreate, BudgetCategoryOut, BudgetCategoryUpdate
from database import get_db
from oauth2 import get_current_user
from typing import List
from core.security import role_required

router = APIRouter(prefix="/budget-categories", tags=["Budget Categories"])


#create budget categories
@router.post("/", response_model=BudgetCategoryOut)
def create_budget_category(category: BudgetCategoryCreate, db:Session = Depends(get_db), current_user = Depends(get_current_user)):
    existing_category = db.query(BudgetCategory).filter(BudgetCategory.user_id == current_user.id, BudgetCategory.name == category.name).first()
    if existing_category:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Category name already exists")
    
    db_category = BudgetCategory(
        user_id = current_user.id,
        name = category.name,
        monthly_limit = category.monthly_limit
    )
    
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category



#get all users categories only admin auditor can access
@router.get("/admin", response_model=List[BudgetCategoryOut])
def get_all_users_categories(current_user:str = Depends(role_required(["admin","auditor"])), db:Session = Depends(get_db)):
    categories = db.query(BudgetCategory).all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No categories found")
    return categories



#get all categories of the current user
@router.get("/categories", response_model=List[BudgetCategoryOut])
def get_all_budget_categories(current_user = Depends(get_current_user), db:Session = Depends(get_db)):
    categories = db.query(BudgetCategory).filter(BudgetCategory.user_id == current_user.id).all()
    if not categories:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No categories found")
    return [
        {
            "id": category.id,
            "name": category.name,
            "monthly_limit": category.monthly_limit,
            "remaining_budget": category.remaining_budget,
            "over_spend": category.over_spend,
            "created_at": category.created_at,
            "updated_at": category.updated_at,
            
        }
        for category in categories
    ]



#get category by category name of current user
@router.get("/{category_name}", response_model=BudgetCategoryOut)
def get_budget_category_by_name(category_name:str, current_user= Depends(get_current_user), db: Session = Depends(get_db)):
    category = db.query(BudgetCategory).filter(BudgetCategory.user_id == current_user.id, BudgetCategory.name == category_name).first()
    if category is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"{category_name} is not found")
    return category


#delete current user category by category name
@router.delete("/delete/{category_name}")
def delete_budget_category(category_name: str, current_user=Depends(get_current_user), db:Session = Depends(get_db)):
    category = db.query(BudgetCategory).filter(BudgetCategory.user_id == current_user.id, BudgetCategory.name == category_name).first()
    if category is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"{category_name} is not found")
    db.delete(category)
    db.flush()
    db.commit()
    return {"message":f"{category_name} deleted successfully"}



#update current user category by category name
@router.put("/update/{category_name}", response_model=BudgetCategoryOut)
def update_budget_category(category_name:str, category_update: BudgetCategoryUpdate, current_user = Depends(get_current_user), db: Session = Depends(get_db)):
    category = db.query(BudgetCategory).filter(BudgetCategory.user_id == current_user.id, BudgetCategory.name == category_name).first()
    
    if category_update.name and category_update.name != category.name:
        existing_category = db.query(BudgetCategory).filter(
            BudgetCategory.user_id == current_user.id, 
            BudgetCategory.name == category_update.name
        ).first()
        if existing_category:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Category name '{category_update.name}' already exists"
            )
    if category is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail= f"{category_name} is not found")
    if category_update.name:
        category.name = category_update.name
    if category_update.monthly_limit:
        category.monthly_limit = category_update.monthly_limit
    
    db.commit()
    db.refresh(category)
    
    return category


#delete category by admin
@router.delete("/admin/{category_id}")
def delete_category_by_admin(category_id:int, current_user: str = Depends(role_required(["admin"])), db: Session = Depends(get_db)):
    category = db.query(BudgetCategory).filter(BudgetCategory.id == category_id ).first()
    if not category:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Category not found")
    db.delete(category)
    db.flush()
    db.commit()
    return {"data": category, "message":"deleted successfully"}
    