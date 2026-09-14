from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    business_name: str

class UserOut(BaseModel):
    id: int
    email: str
    business_name: str
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
