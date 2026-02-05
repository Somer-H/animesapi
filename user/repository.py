from sqlalchemy.orm import Session
from user.models import User


class UserRepository:
    """Repositorio para manejar operaciones de Usuario en la base de datos"""
    
    @staticmethod
    def create(db: Session, username: str, email: str, hashed_password: str) -> User:
        """Crea un nuevo usuario en la base de datos"""
        user = User(
            username=username,
            email=email,
            hashed_password=hashed_password
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_by_username(db: Session, username: str) -> User:
        """Obtiene un usuario por nombre de usuario"""
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> User:
        """Obtiene un usuario por ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> User:
        """Obtiene un usuario por email"""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> list:
        """Obtiene todos los usuarios con paginación"""
        return db.query(User).offset(skip).limit(limit).all()
