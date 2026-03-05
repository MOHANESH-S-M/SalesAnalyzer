from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, or_
from app.db.session import get_db
from app.models.base import User
from app.schemas.user_schema import UserCreate, UserLogin, UserResponse
from app.core.security import get_password_hash, verify_password

router = APIRouter()

@router.post("/register", response_model=UserResponse)
async def register(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    # Check if user already exists
    query = select(User).where(
        or_(
            User.email == user_in.email,
            User.phone_number == user_in.phone_number
        )
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or phone number already exists."
        )
    
    # Create new user
    new_user = User(
        name=user_in.name,
        email=user_in.email,
        phone_number=user_in.phone_number,
        password=get_password_hash(user_in.password),
        city=user_in.city,
        state=user_in.state
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(login_data: UserLogin, db: AsyncSession = Depends(get_db)):
    # Find user by name, email, or phone number
    query = select(User).where(
        or_(
            User.name == login_data.username_or_email_or_phone,
            User.email == login_data.username_or_email_or_phone,
            User.phone_number == login_data.username_or_email_or_phone
        )
    )
    result = await db.execute(query)
    user = result.scalar_one_or_none()

    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    return {"message": "Login successful", "user": {"id": user.id, "name": user.name}}
