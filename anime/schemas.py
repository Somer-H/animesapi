from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnimeCreate(BaseModel):
    titulo: str
    genero: str
    año: int
    descripcion: str
    image_url: Optional[str] = None


class AnimeUpdate(BaseModel):
    titulo: str = None
    genero: str = None
    año: int = None
    descripcion: str = None
    image_url: Optional[str] = None


class AnimeResponse(BaseModel):
    id: int
    titulo: str
    genero: str
    año: int
    descripcion: str
    image_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
