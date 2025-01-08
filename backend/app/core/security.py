from passlib.context import CryptContext
import re
from fastapi import HTTPException, status

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