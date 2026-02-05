from pydantic import BaseModel
from datetime import datetime


class AnimeCreate(BaseModel):
    """Schema para crear un anime"""
    titulo: str
    genero: str
    año: int
    descripcion: str


class AnimeUpdate(BaseModel):
    """Schema para actualizar un anime"""
    titulo: str = None
    genero: str = None
    año: int = None
    descripcion: str = None


class AnimeResponse(BaseModel):
    """Schema de respuesta del anime"""
    id: int
    titulo: str
    genero: str
    año: int
    descripcion: str
    created_at: datetime
    
    class Config:
        from_attributes = True
