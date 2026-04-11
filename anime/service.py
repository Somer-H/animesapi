from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from anime.repository import AnimeRepository
from anime.schemas import AnimeCreate, AnimeUpdate


class AnimeService:
    
    @staticmethod
    def create_anime(db: Session, anime_create: AnimeCreate, user_id: int):
        existing_anime = AnimeRepository.get_by_titulo(db, anime_create.titulo)
        if existing_anime:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Ya existe un anime con ese título"
            )
        
        return AnimeRepository.create(
            db,
            titulo=anime_create.titulo,
            genero=anime_create.genero,
            año=anime_create.año,
            descripcion=anime_create.descripcion,
            image_url=anime_create.image_url,
            user_id=user_id
        )
    
    @staticmethod
    def get_anime_by_id(db: Session, anime_id: int):
        anime = AnimeRepository.get_by_id(db, anime_id)
        
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anime no encontrado"
            )
        
        return anime
    
    @staticmethod
    def get_all_animes(db: Session, skip: int = 0, limit: int = 10):
        return AnimeRepository.get_all(db, skip, limit)
    
    @staticmethod
    def update_anime(db: Session, anime_id: int, anime_update: AnimeUpdate):
        anime = AnimeRepository.get_by_id(db, anime_id)
        
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anime no encontrado"
            )
        
        update_data = anime_update.dict(exclude_unset=True)
        return AnimeRepository.update(db, anime_id, **update_data)
    
    @staticmethod
    def delete_anime(db: Session, anime_id: int):
        success = AnimeRepository.delete(db, anime_id)
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Anime no encontrado"
            )
        
        return {"message": "Anime eliminado correctamente"}
