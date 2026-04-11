from sqlalchemy.orm import Session, joinedload
from watchlist.models import Watchlist


class WatchlistRepository:
    
    @staticmethod
    def add_or_update(db: Session, user_id: int, anime_id: int, estado: str) -> Watchlist:
        item = db.query(Watchlist).filter(
            Watchlist.user_id == user_id, 
            Watchlist.anime_id == anime_id
        ).first()
        
        if item:
            item.estado = estado
        else:
            item = Watchlist(user_id=user_id, anime_id=anime_id, estado=estado)
            db.add(item)
            
        db.commit()
        db.refresh(item)
        return item
    
    @staticmethod
    def get_user_watchlist(db: Session, user_id: int) -> list:
        return db.query(Watchlist).options(joinedload(Watchlist.anime)).filter(Watchlist.user_id == user_id).all()

    @staticmethod
    def remove(db: Session, user_id: int, anime_id: int) -> bool:
        item = db.query(Watchlist).filter(
            Watchlist.user_id == user_id, 
            Watchlist.anime_id == anime_id
        ).first()
        if item:
            db.delete(item)
            db.commit()
            return True
        return False
