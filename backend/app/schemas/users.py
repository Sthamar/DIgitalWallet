from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: Optional[str] = "user"
    
    
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    role: str
    
    class Config:
        from_attribute = True
    
class UserUpdate(BaseModel):
    username: str
    role: str
    
class PasswordUpdate(BaseModel):
    current_password: str
    new_password: str