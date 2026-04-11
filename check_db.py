from config.database import SessionLocal
from anime.models import Anime

def check_animes():
    db = SessionLocal()
    try:
        animes = db.query(Anime).all()
        print(f"Total animes: {len(animes)}")
        for a in animes:
            print(f"ID: {a.id}, Title: {a.titulo}")
    finally:
        db.close()

if __name__ == "__main__":
    check_animes()
