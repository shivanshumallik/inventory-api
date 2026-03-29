# app/schemas/user.py

from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from app.models.user import UserRole


class UserRegister(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    full_name: str = Field(..., min_length=2, max_length=100)
    password: str = Field(..., min_length=6, description="Minimum 6 characters")
    role: UserRole = Field(default=UserRole.STAFF)


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: str
    full_name: str
    role: UserRole
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    # --- IMPORTANT ---
    # OAuth2 standard requires EXACTLY these field names
    # 'access_token' and 'token_type' must be present
    access_token: str
    token_type: str = "bearer"
    user: UserResponse