from fastapi import APIRouter, HTTPException, status, Depends
from models.users import User
from schemas.users import UserCreate, UserOut, UserUpdate
from database import get_db
from sqlalchemy.orm import Session
from typing import List
from core.security import hash_password, verify_password, validate_password


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
            db_user = User(username = user.username, email = user.email, password_hash = hashed_password)
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        
    
    
    
           
