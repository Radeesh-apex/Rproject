from fastapi import FastAPI
from app.api.auth import auth

app = FastAPI()

# prefix ensures your URLs look like: /api/v1/auth/login
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])