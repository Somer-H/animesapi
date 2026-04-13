from sqlalchemy.orm import Session
from anime.models import Anime


class AnimeRepository:
    
    @staticmethod
    def create(db: Session, titulo: str, genero: str, año: int, descripcion: str, user_id: int, image_url: str = None, tags: str = "") -> Anime:
        anime = Anime(
            titulo=titulo,
            genero=genero,
            año=año,
            descripcion=descripcion,
            image_url=image_url,
            tags=tags,
            user_id=user_id
        )
        db.add(anime)
        db.commit()
        db.refresh(anime)
        return anime
    
    @staticmethod
    def get_by_id(db: Session, anime_id: int) -> Anime:
        return db.query(Anime).filter(Anime.id == anime_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 10) -> list:
        return db.query(Anime).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_titulo(db: Session, titulo: str) -> Anime:
        return db.query(Anime).filter(Anime.titulo == titulo).first()
    
    @staticmethod
    def update(db: Session, anime_id: int, **kwargs) -> Anime:
        anime = db.query(Anime).filter(Anime.id == anime_id).first()
        if anime:
            for key, value in kwargs.items():
                if value is not None:
                    setattr(anime, key, value)
            db.commit()
            db.refresh(anime)
        return anime
    
    @staticmethod
    def like(db: Session, anime_id: int) -> Anime:
        anime = db.query(Anime).filter(Anime.id == anime_id).first()
        if anime:
            anime.likes += 1
            db.commit()
            db.refresh(anime)
        return anime
    
    @staticmethod
    def delete(db: Session, anime_id: int) -> bool:
        anime = db.query(Anime).filter(Anime.id == anime_id).first()
        if anime:
            db.delete(anime)
            db.commit()
            return True
        return False
