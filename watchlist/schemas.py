from pydantic import BaseModel
from datetime import datetime


class WatchlistCreate(BaseModel):
    anime_id: int
    estado: str


class WatchlistResponse(BaseModel):
    id: int
    user_id: int
    anime_id: int
    estado: str
    updated_at: datetime
    
    class Config:
        from_attributes = True
