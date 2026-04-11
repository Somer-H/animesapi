from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from config.database import get_db
from watchlist.schemas import WatchlistCreate, WatchlistResponse
from watchlist.service import WatchlistService
from security.auth import verify_token

router = APIRouter(prefix="/api/watchlist", tags=["watchlist"])


@router.post("/", response_model=WatchlistResponse)
def update_watchlist(
    data: WatchlistCreate, 
    db: Session = Depends(get_db), 
    payload: dict = Depends(verify_token)
):
    user_id = int(payload.get("sub"))
    return WatchlistService.update_watchlist(db, user_id, data)


@router.get("/me", response_model=list[WatchlistResponse])
def get_my_watchlist(db: Session = Depends(get_db), payload: dict = Depends(verify_token)):
    user_id = int(payload.get("sub"))
    return WatchlistService.get_my_list(db, user_id)


@router.get("/user/{user_id}", response_model=list[WatchlistResponse])
def get_user_watchlist(user_id: int, db: Session = Depends(get_db)):
    return WatchlistService.get_my_list(db, user_id)


@router.delete("/{anime_id}")
def remove_from_watchlist(
    anime_id: int, 
    db: Session = Depends(get_db), 
    payload: dict = Depends(verify_token)
):
    user_id = int(payload.get("sub"))
    WatchlistService.remove_from_list(db, user_id, anime_id)
    return {"message": "Anime eliminado de la lista"}
