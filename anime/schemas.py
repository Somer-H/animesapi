from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AnimeCreate(BaseModel):
    titulo: str
    genero: str
    año: int
    descripcion: str
    image_url: Optional[str] = None
    tags: Optional[str] = ""  # Tags separados por coma: "accion,romance,comedia"


class AnimeUpdate(BaseModel):
    titulo: str = None
    genero: str = None
    año: int = None
    descripcion: str = None
    image_url: Optional[str] = None
    tags: Optional[str] = None  # Tags separados por coma


class AnimeResponse(BaseModel):
    id: int
    titulo: str
    genero: str
    año: int
    descripcion: str
    image_url: Optional[str]
    tags: Optional[str] = ""
    user_id: int
    created_at: datetime
    
    class Config:
        from_attributes = True
