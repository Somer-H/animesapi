from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from anime.schemas import AnimeResponse


class WatchlistCreate(BaseModel):
    anime_id: int
    estado: str


class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    anime_id: int
    estado: str
    updated_at: datetime
    anime: Optional[AnimeResponse] = None
    
    class Config:
        from_attributes = True
