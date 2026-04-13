from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from config.database import Base


class Anime(Base):
    __tablename__ = "animes"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), index=True, nullable=False)
    genero = Column(String(50), nullable=False)
    año = Column(Integer, nullable=False)
    descripcion = Column(String(500), nullable=False)
    image_url = Column(String(500), nullable=True)
    # Tags separados por coma: "accion,romance,comedia"
    tags = Column(String(500), nullable=True, default="")
    likes = Column(Integer, default=0)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relaciones
    watchlist_entries = relationship("Watchlist", back_populates="anime", cascade="all, delete-orphan")
    owner = relationship("User", back_populates="animes")
