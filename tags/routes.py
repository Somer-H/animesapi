from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from security.auth import verify_token
from tags.schemas import TagSubscribeRequest, TagSubscriptionResponse, MyTagsResponse
from tags.repository import TagRepository

router = APIRouter(prefix="/api/tags", tags=["tags"])


@router.post("/subscribe", response_model=TagSubscriptionResponse, status_code=201)
def subscribe_to_tag(
    request: TagSubscribeRequest,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    """Suscribirse a un tag para recibir notificaciones cuando se publique un anime con ese tag."""
    user_id = int(payload.get("sub"))
    tag = request.tag.strip()
    if not tag:
        raise HTTPException(status_code=400, detail="El tag no puede estar vacío")
    return TagRepository.subscribe(db, user_id, tag, request.fcm_token)


@router.delete("/unsubscribe/{tag}", status_code=200)
def unsubscribe_from_tag(
    tag: str,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    """Desuscribirse de un tag."""
    user_id = int(payload.get("sub"))
    success = TagRepository.unsubscribe(db, user_id, tag)
    if not success:
        raise HTTPException(status_code=404, detail="No estás suscrito a ese tag")
    return {"message": f"Desuscrito del tag '{tag}' correctamente"}


@router.get("/mine", response_model=MyTagsResponse)
def get_my_tags(
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    """Devuelve la lista de tags a los que el usuario actual está suscrito."""
    user_id = int(payload.get("sub"))
    tags = TagRepository.get_user_tags(db, user_id)
    return MyTagsResponse(tags=tags)
