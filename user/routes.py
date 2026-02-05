from fastapi import APIRouter, Depends, HTTPException, status
from datetime import timedelta
from sqlalchemy.orm import Session
from config.database import get_db
from config.settings import ACCESS_TOKEN_EXPIRE_MINUTES
from user.schemas import UserCreate, UserLogin, UserResponse, TokenResponse
from user.service import UserService
from security.auth import create_access_token, verify_token

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("/register", response_model=UserResponse)
def register(user_create: UserCreate, db: Session = Depends(get_db)):
    """Registra un nuevo usuario"""
    user = UserService.create_user(db, user_create)
    return user


@router.post("/login", response_model=TokenResponse)
def login(user_login: UserLogin, db: Session = Depends(get_db)):
    """Autentica un usuario y devuelve un token JWT"""
    user = UserService.authenticate_user(db, user_login)
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(user.id)},
        expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
def get_current_user(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    """Obtiene el usuario autenticado actual"""
    user_id = payload.get("sub")
    user = UserService.get_user_by_id(db, user_id)
    return user
