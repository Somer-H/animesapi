from pydantic import BaseModel
from datetime import datetime


class AnimeCreate(BaseModel):
    titulo: str
    genero: str
    año: int
    descripcion: str


class AnimeUpdate(BaseModel):
    titulo: str = None
    genero: str = None
    año: int = None
    descripcion: str = None


class AnimeResponse(BaseModel):
    id: int
    titulo: str
    genero: str
    año: int
    descripcion: str
    created_at: datetime
    
    class Config:
        from_attributes = True
