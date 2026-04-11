from sqlalchemy import Column, Integer, String, DateTime
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
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    # Relación con Watchlist con borrado en cascada
    watchlist_entries = relationship("Watchlist", back_populates="anime", cascade="all, delete-orphan")
