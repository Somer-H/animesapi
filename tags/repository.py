from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from tags.models import UserTagSubscription


class TagRepository:

    @staticmethod
    def subscribe(db: Session, user_id: int, tag: str, fcm_token: str = None) -> UserTagSubscription:
        """Suscribe a un usuario a un tag. Actualiza el fcm_token si ya existe."""
        existing = db.query(UserTagSubscription).filter(
            UserTagSubscription.user_id == user_id,
            UserTagSubscription.tag == tag.lower().strip()
        ).first()

        if existing:
            # Actualizar el fcm_token si cambió
            if fcm_token:
                existing.fcm_token = fcm_token
                db.commit()
                db.refresh(existing)
            return existing

        subscription = UserTagSubscription(
            user_id=user_id,
            tag=tag.lower().strip(),
            fcm_token=fcm_token
        )
        db.add(subscription)
        db.commit()
        db.refresh(subscription)
        return subscription

    @staticmethod
    def unsubscribe(db: Session, user_id: int, tag: str) -> bool:
        """Desuscribe a un usuario de un tag."""
        subscription = db.query(UserTagSubscription).filter(
            UserTagSubscription.user_id == user_id,
            UserTagSubscription.tag == tag.lower().strip()
        ).first()
        if subscription:
            db.delete(subscription)
            db.commit()
            return True
        return False

    @staticmethod
    def get_user_tags(db: Session, user_id: int) -> list[str]:
        """Devuelve la lista de tags suscritos por un usuario."""
        subs = db.query(UserTagSubscription).filter(
            UserTagSubscription.user_id == user_id
        ).all()
        return [s.tag for s in subs]

    @staticmethod
    def get_fcm_tokens_for_tags(db: Session, tags: list[str]) -> list[str]:
        """Dado un conjunto de tags, devuelve todos los fcm_tokens de usuarios suscritos."""
        normalized = [t.lower().strip() for t in tags]
        subs = db.query(UserTagSubscription).filter(
            UserTagSubscription.tag.in_(normalized),
            UserTagSubscription.fcm_token.isnot(None)
        ).all()
        # Evitar duplicados si un usuario está suscrito a varios tags del anime
        return list({s.fcm_token for s in subs})
