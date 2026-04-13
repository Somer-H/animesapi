from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from config.database import get_db
from anime.schemas import AnimeCreate, AnimeUpdate, AnimeResponse
from anime.service import AnimeService
from security.auth import verify_token
import cloudinary.uploader
from tags.repository import TagRepository
from tags.notifications import send_push_notification


router = APIRouter(prefix="/api/animes", tags=["animes"])


@router.post("", response_model=AnimeResponse)
def create_anime(
    anime_create: AnimeCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    user_id = int(payload.get("sub"))
    print(f"[CREATE] user_id from token: {user_id} (type: {type(user_id)})") 
    anime = AnimeService.create_anime(db, anime_create, user_id)

    # 2. Notificar a usuarios interesados via FCM (basado en tags)
    if anime.tags:
        try:
            tags_list = [t.strip().lower() for t in anime.tags.split(",") if t.strip()]
            print(f"DEBUG: Buscando tokens para tags: {tags_list} excluyendo autor: {user_id}")
            tokens = TagRepository.get_fcm_tokens_for_tags(db, tags_list, exclude_user_id=user_id)
            print(f"DEBUG: Tokens encontrados: {len(tokens)}")
            
            if tokens:
                success = send_push_notification(
                    fcm_tokens=tokens,
                    title="Nuevo Anime publicado",
                    body=f"¡Se ha publicado '{anime.titulo}'!",
                    data={
                        "anime_id": anime.id,
                        "tags": anime.tags,
                        "actions": "view,dismiss"
                    }
                )
                if success:
                    print("DEBUG: Notificaciones enviadas exitosamente vía Firebase.")
                else:
                    print("DEBUG: Hubo problemas al enviar las notificaciones (revisa logs de FCM arriba).")
            else:
                print("DEBUG: No se encontraron usuarios suscritos a estos tags.")
        except Exception as e:
            print(f"ERROR en el disparador de notificaciones: {e}")

    return anime


@router.get("/{anime_id}", response_model=AnimeResponse)
def get_anime(
    anime_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    return AnimeService.get_anime_by_id(db, anime_id)


@router.get("", response_model=list[AnimeResponse])
def get_all_animes(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 1000,
    payload: dict = Depends(verify_token)
):
    return AnimeService.get_all_animes(db, skip, limit)


@router.put("/{anime_id}", response_model=AnimeResponse)
def update_anime(
    anime_id: int,
    anime_update: AnimeUpdate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    user_id = int(payload.get("sub"))
    anime = AnimeService.get_anime_by_id(db, anime_id)
    
    if int(anime.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para editar este anime"
        )
        
    return AnimeService.update_anime(db, anime_id, anime_update)


@router.delete("/{anime_id}")
def delete_anime(
    anime_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    user_id = int(payload.get("sub"))
    anime = AnimeService.get_anime_by_id(db, anime_id)
    
    if int(anime.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para eliminar este anime"
        )
        
    return AnimeService.delete_anime(db, anime_id)


@router.post("/{anime_id}/upload", response_model=AnimeResponse)
def upload_anime_image(
    anime_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    user_id = int(payload.get("sub"))
    # Obtener el anime para verificar que existe y es el dueño
    anime = AnimeService.get_anime_by_id(db, anime_id)
    
    print(f"[UPLOAD] anime.user_id: {anime.user_id} (type: {type(anime.user_id)}) | token user_id: {user_id} (type: {type(user_id)})")
    
    if int(anime.user_id) != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tienes permiso para subir imágenes a este anime"
        )
    
    # Subir a Cloudinary
    upload_result = cloudinary.uploader.upload(file.file)
    image_url = upload_result.get("secure_url")
    
    # Actualizar la base de datos
    anime_update = AnimeUpdate(image_url=image_url)
    return AnimeService.update_anime(db, anime_id, anime_update)


@router.post("/{anime_id}/like", response_model=AnimeResponse)
def like_anime(
    anime_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    user_id_liking = int(payload.get("sub"))
    anime = AnimeService.like_anime(db, anime_id)
    
    # 2. Notificar al dueño del anime (si no es quien le dio like)
    if int(anime.user_id) != user_id_liking:
        try:
            tokens = TagRepository.get_fcm_tokens_for_user(db, anime.user_id)
            if tokens:
                send_push_notification(
                    fcm_tokens=tokens,
                    title="¡Nuevo Like!",
                    body=f"A alguien le gustó tu anime: {anime.titulo}",
                    data={
                        "anime_id": anime.id,
                        "type": "like"
                    }
                )
        except Exception as e:
            print(f"ERROR enviando notificación de like: {e}")
            
    return anime
