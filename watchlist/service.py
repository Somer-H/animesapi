from sqlalchemy.orm import Session
from watchlist.repository import WatchlistRepository
from watchlist.schemas import WatchlistCreate


class WatchlistService:
    
    @staticmethod
    def update_watchlist(db: Session, user_id: int, data: WatchlistCreate):
        return WatchlistRepository.add_or_update(
            db, user_id, data.anime_id, data.estado
        )
    
    @staticmethod
    def get_my_list(db: Session, user_id: int):
        return WatchlistRepository.get_user_watchlist(db, user_id)

    @staticmethod
    def remove_from_list(db: Session, user_id: int, anime_id: int):
        return WatchlistRepository.remove(db, user_id, anime_id)
