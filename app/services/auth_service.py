from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.models import User
from app.core.security import hash_password, verify_password, create_access_token
from fastapi import HTTPException, status

class AuthService:
    @staticmethod
    async def register_user(db: AsyncSession, user_data):
        # Check if email exists
        result = await db.execute(select(User).where(User.email == user_data.email))
        if result.scalar_one_or_none():
            raise HTTPException(status_code=400, detail="Email already registered")
        
        new_user = User(
            email=user_data.email,
            name=user_data.name,
            password_hash=hash_password(user_data.password),
            role=user_data.role # 'customer', 'seller', or 'admin'
        )
        db.add(new_user)
        await db.commit()
        await db.refresh(new_user)
        return new_user

    @staticmethod
    async def authenticate_user(db: AsyncSession, email, password):
        result = await db.execute(select(User).where(User.email == email))
        user = result.scalar_one_or_none()
        
        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create token including the ROLE in the payload
        token = create_access_token(data={"sub": user.email, "role": user.role})
        return {"access_token": token, "token_type": "bearer"}