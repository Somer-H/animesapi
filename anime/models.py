from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone
from config.database import Base


class Anime(Base):
    __tablename__ = "animes"
    
    id = Column(Integer, primary_key=True, index=True)
    titulo = Column(String(150), index=True, nullable=False)
    genero = Column(String(50), nullable=False)
    año = Column(Integer, nullable=False)
    descripcion = Column(String(500), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
