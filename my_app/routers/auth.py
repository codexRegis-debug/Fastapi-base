from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from my_app.schemas import schemas
from my_app.data import my_base
from my_app.models import models
import asyncio

router = APIRouter(tags=['Auth'])

@router.post("/signup", response_model=schemas.UserOut)
async def signup(
    user: schemas.UserCreate,
    db: AsyncSession = Depends(my_base.get_db)
):
    try:
        stmt = select(models.User).where(models.User.useremail == user.useremail)
        result = await db.execute(stmt)
        db_user = result.scalar_one_or_none()
        # db_user = await db.query(models.User).filter(models.User.email == user.email).first()
        if db_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        hashed_password = auth.get_password_hash(user.userpassword)
        new_user = models.User(
            username=username,
            useremail=user.email,
            hashed_password=hashed_password,
        )
    except Exception as e:
        print(f'Signup failed: {e}')

        raise HTTPException(status_code=500, detail=str(e))

    db.add()
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login", response_model=schemas.Token)
async def login(
    form_data: schemas.UserLogin,
    db: AsyncSession = Depends(my_base.get_db)
):
    try:
        statetments = select(models.User).where(models.User.useremail == form_data.useremail)
        result = await db.execute(statetments)
        user = result.scalar_one_or_none()
        # user = db.query(models.User).filter(models.User.email == user.email).first()
        if not user or not auth.verify_password(form_data.userpassword, user.hashed_password):
            raise HTTPException(
                status_code=401,
                detail="Invalid credentials"
            )

        access_token = auth.create_access_token(data={"user_id": user.id})
        return {
            "access_tokens": access_token,
            "token_type": "bearer"
        }

    except Exception as e:
        print(f'Login failed: {e}')

        raise HTTPException(status_code=500, detail=str(e))


@router.get('/users', response_model=schemas.Token) # Not sure but come later to debug
async def read_users():
    pass #  come later to debug
