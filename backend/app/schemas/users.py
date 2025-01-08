from pydantic import BaseModel, EmailStr
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    
    
class UserOut(BaseModel):
    id: int
    username: str
    email: EmailStr
    
    class Config:
        from_attribute = True
    
class UserUpdate(BaseModel):
    username: str
    email: EmailStr
    