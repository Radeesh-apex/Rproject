from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
from app.models.models import UserRole

# Shared properties
class UserBase(BaseModel):
    email: EmailStr
    name: str
    phone: Optional[str] = None
    role: UserRole = UserRole.customer

# Properties to receive via API on registration
class UserCreate(UserBase):
    password: str

# Properties to return via API (Hides the password!)
class UserOut(UserBase):
    user_id: int
    uuid: Optional[str] = None

    # This allows Pydantic to read data from SQLAlchemy objects
    model_config = ConfigDict(from_attributes=True)