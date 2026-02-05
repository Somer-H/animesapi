from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from user.repository import UserRepository
from user.schemas import UserCreate, UserLogin
from security.auth import hash_password, verify_password


class UserService:
    """Servicio de negocio para Usuario"""
    
    @staticmethod
    def create_user(db: Session, user_create: UserCreate):
        """Crea un nuevo usuario después de validar que no exista"""
        # Verificar si el usuario ya existe
        existing_user = UserRepository.get_by_username(db, user_create.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El usuario ya existe"
            )
        
        # Verificar si el email ya existe
        existing_email = UserRepository.get_by_email(db, user_create.email)
        if existing_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="El email ya está registrado"
            )
        
        # Encriptar contraseña
        hashed_password = hash_password(user_create.password)
        
        # Crear usuario
        return UserRepository.create(
            db,
            username=user_create.username,
            email=user_create.email,
            hashed_password=hashed_password
        )
    
    @staticmethod
    def authenticate_user(db: Session, user_login: UserLogin):
        """Autentica un usuario y devuelve el usuario si es válido"""
        user = UserRepository.get_by_username(db, user_login.username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        # Verificar contraseña
        if not verify_password(user_login.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario o contraseña incorrectos"
            )
        
        return user
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int):
        """Obtiene un usuario por ID"""
        user = UserRepository.get_by_id(db, user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuario no encontrado"
            )
        
        return user
