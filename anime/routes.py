from fastapi import APIRouter, Depends, UploadFile, File
from sqlalchemy.orm import Session
from config.database import get_db
from anime.schemas import AnimeCreate, AnimeUpdate, AnimeResponse
from anime.service import AnimeService
from security.auth import verify_token
import cloudinary.uploader


router = APIRouter(prefix="/api/animes", tags=["animes"])


@router.post("", response_model=AnimeResponse)
def create_anime(
    anime_create: AnimeCreate,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    return AnimeService.create_anime(db, anime_create)


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
    limit: int = 10,
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
    return AnimeService.update_anime(db, anime_id, anime_update)


@router.delete("/{anime_id}")
def delete_anime(
    anime_id: int,
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    return AnimeService.delete_anime(db, anime_id)


@router.post("/{anime_id}/upload", response_model=AnimeResponse)
def upload_anime_image(
    anime_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    payload: dict = Depends(verify_token)
):
    # Obtener el anime para verificar que existe
    anime = AnimeService.get_anime_by_id(db, anime_id)
    
    # Subir a Cloudinary
    upload_result = cloudinary.uploader.upload(file.file)
    image_url = upload_result.get("secure_url")
    
    # Actualizar la base de datos
    anime_update = AnimeUpdate(image_url=image_url)
    return AnimeService.update_anime(db, anime_id, anime_update)
