from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from models.users import User
from schemas import users, token
from core.security import hash_password, verify_password
from oauth2 import create_access_token, get_current_user
from database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix='/auth', tags=["auth"])

@router.post("/login", response_model=token.Token)
def login(userdetails: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    user = db.query(User).filter(User.username == userdetails.username).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The user does not exist.")
    if not verify_password(userdetails.password,user.password_hash):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password.")
    access_token = create_access_token(data = {"user_id": user.id})
    return {"access_token":access_token, "token_type":"bearer"}

@router.get("/me", response_model=users.UserOut)
def get_me(current_user: User = Depends(get_current_user)):
    return current_user