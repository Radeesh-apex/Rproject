#api\auth\api.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.services.auth_service import AuthService
from app.schemas.user_schema import UserCreate, UserOut

router = APIRouter()

@router.post("/register", response_model=UserOut)
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await AuthService.register_user(db, user)

@router.post("/login")
async def login(user_credentials: UserCreate, db: AsyncSession = Depends(get_db)):
    # Note: In production, use OAuth2PasswordRequestForm for standard login
    return await AuthService.authenticate_user(db, user_credentials.email, user_credentials.password)

# --- ROLE BASED PROTECTION EXAMPLE ---
def RoleChecker(allowed_roles: list):
    async def check(token: str = Depends(oauth2_scheme)):
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_role = payload.get("role")
        if user_role not in allowed_roles:
            raise HTTPException(status_code=403, detail="Not enough permissions")
        return payload
    return check

@router.get("/admin-only-data", dependencies=[Depends(RoleChecker(["admin"]))])
async def get_admin_stats():
    return {"data": "Secret Admin Stats"}