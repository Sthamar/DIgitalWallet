from fastapi import APIRouter, HTTPException, status, Depends
from models.users import User
from schemas.users import UserCreate, UserOut, UserUpdate
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from core.security import hash_password, verify_password, validate_password, role_required


router = APIRouter(prefix="/users", tags=['users'])

@router.post("/", response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    if validate_password(user.password):
        hashed_password = hash_password(user.password)   
        existing_email = db.query(User).filter(User.email == user.email).first()
        existing_username = db.query(User).filter(User.username == user.username).first()
        if existing_email or existing_username:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="user already exist ")  
        else:
            db_user = User(username = user.username, email = user.email, password_hash = hashed_password, role = user.role)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        
        
@router.get("/{username}", response_model=UserOut)
def get_user_by_username(username: str, db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found.")
    else:
        return user
    
@router.get("/admin/users",response_model=List[UserOut])
def get_all_users(
    current_user: User = Depends(role_required("admin")),
    db: Session = Depends(get_db)
):
    users = db.query(User).all()
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No users found")
    return users
        
        
    
    
    
           
