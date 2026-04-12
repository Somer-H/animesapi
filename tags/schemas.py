from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TagSubscribeRequest(BaseModel):
    tag: str
    fcm_token: Optional[str] = None  # Token FCM del dispositivo para notificaciones push


class TagSubscriptionResponse(BaseModel):
    id: int
    user_id: int
    tag: str
    fcm_token: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class MyTagsResponse(BaseModel):
    tags: list[str]
