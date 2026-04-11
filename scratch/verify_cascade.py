from sqlalchemy.orm import Session
from config.database import SessionLocal, engine, Base
from anime.models import Anime
from watchlist.models import Watchlist
from user.models import User
import uuid

def test_cascade_deletion():
    db = SessionLocal()
    try:
        # 1. Crear usuario de prueba
        username = f"testuser_{uuid.uuid4().hex[:6]}"
        user = User(username=username, email=f"{username}@test.com", hashed_password="hashed_password")
        db.add(user)
        db.commit()
        db.refresh(user)
        print(f"Usuario creado: {user.id}")

        # 2. Crear anime de prueba
        anime = Anime(titulo=f"Test Anime {uuid.uuid4().hex[:6]}", genero="Test", año=2024, descripcion="Test desc")
        db.add(anime)
        db.commit()
        db.refresh(anime)
        print(f"Anime creado: {anime.id}")

        # 3. Añadir anime a la watchlist del usuario
        watchlist_entry = Watchlist(user_id=user.id, anime_id=anime.id, estado="viendo")
        db.add(watchlist_entry)
        db.commit()
        db.refresh(watchlist_entry)
        print(f"Entrada de Watchlist creada: {watchlist_entry.id}")

        # 4. Intentar eliminar el anime
        print(f"Intentando eliminar anime {anime.id}...")
        db.delete(anime)
        db.commit()
        print("Anime eliminado exitosamente (CASCADE).")

        # 5. Verificar que la entrada de watchlist también desapareció
        check_entry = db.query(Watchlist).filter(Watchlist.id == watchlist_entry.id).first()
        if check_entry is None:
            print("¡ÉXITO! La entrada de la watchlist fue eliminada automáticamente.")
        else:
            print("ERROR: La entrada de la watchlist todavía existe.")

    except Exception as e:
        print(f"ERROR durante la prueba: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    test_cascade_deletion()
