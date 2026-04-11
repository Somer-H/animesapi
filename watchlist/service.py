from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from watchlist.repository import WatchlistRepository
from watchlist.schemas import WatchlistCreate
from anime.repository import AnimeRepository


class WatchlistService:
    
    @staticmethod
    def update_watchlist(db: Session, user_id: int, data: WatchlistCreate):
        # Verificar que el anime exista antes de agregarlo
        anime = AnimeRepository.get_by_id(db, data.anime_id)
        if not anime:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"El anime con ID {data.anime_id} no existe"
            )
            
        return WatchlistRepository.add_or_update(
            db, user_id, data.anime_id, data.estado
        )
    
    @staticmethod
    def get_my_list(db: Session, user_id: int):
        return WatchlistRepository.get_user_watchlist(db, user_id)

    @staticmethod
    def remove_from_list(db: Session, user_id: int, anime_id: int):
        return WatchlistRepository.remove(db, user_id, anime_id)
