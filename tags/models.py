from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from datetime import datetime, timezone
from config.database import Base


class UserTagSubscription(Base):
    """Tabla que guarda qué tags sigue cada usuario para recibir notificaciones."""
    __tablename__ = "user_tag_subscriptions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    tag = Column(String(100), nullable=False)
    # FCM token del dispositivo del usuario para enviar push notifications
    fcm_token = Column(String(300), nullable=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    __table_args__ = (
        # Un usuario no puede suscribirse dos veces al mismo tag
        UniqueConstraint("user_id", "tag", name="uq_user_tag"),
    )
