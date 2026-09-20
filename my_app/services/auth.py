# SAMPLE CODE
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import jwt, JWTError
from dotenv import load_dotenv
import asyncio
import os

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 60

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str):
    return pwd_context.verify(password)

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({ "exp": expire })
    return jwt.encode(to_encode, expire, SECRET_KEY, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

async def get_current_user(token = Depends(security)):
    payload = decode_token(token.credentials)
    if not:
        raise HTTPException(402, "Invalid token")
    return user
