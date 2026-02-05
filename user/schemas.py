from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    """Schema para crear un usuario"""
    username: str
    email: EmailStr
    password: str


class UserLogin(BaseModel):
    """Schema para el login"""
    username: str
    password: str


class UserResponse(BaseModel):
    """Schema de respuesta del usuario"""
    id: int
    username: str
    email: str
    created_at: datetime
    
    class Config:
        from_attributes = True


class TokenResponse(BaseModel):
    """Schema de respuesta del token"""
    access_token: str
    token_type: str
    user: UserResponse
