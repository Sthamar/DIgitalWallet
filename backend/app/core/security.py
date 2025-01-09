from passlib.context import CryptContext
import re
from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from oauth2 import get_current_user

pwd_context = CryptContext(schemes=["bcrypt"], deprecated = 'auto')

def hash_password(password: str) -> str:
    """hash password"""
    return pwd_context.hash(password)

def verify_password(hashed_password: str, password: str)-> bool:
    """check hashed password and password"""
    return pwd_context.verify(hashed_password, password)

def validate_password(password: str):
    if len(password) < 8:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must be at least 8 characters long.")
    if not re.search(r'[A-Z]', password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one uppercase letter.")
    if not re.search(r'[a-z]', password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one lowercase letter.")
    if not re.search(r'[0-9]', password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one number.")
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password must contain at least one special character.")
    return True


def role_required(required_role: list[str]):
    def wrapper(current_user: User = Depends(get_current_user), db:Session = Depends(get_db)):
        if current_user.role not in required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"user role '{current_user.role}' does not have access to this"
            )
        return current_user
    return wrapper