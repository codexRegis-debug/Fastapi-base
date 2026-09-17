from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    useremail: EmailStr
    userpassword: str
    username: str

class UserOut(BaseModel):
    username: str
    useremail: EmailStr
    userpassword: str
    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class InvoiceCreate(BaseModel):
    amount: float
    description: str
    client_id: str

class InvoiceOut(BaseModel):
    id: int
    status: str
    created_at: datetime
    class Config:
        from_attributes = True
