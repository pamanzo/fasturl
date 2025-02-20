from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.auth_logic import verify_user_logged_in
from app.database import get_db
from app.models import User, URL
from app.schemas import URLListResponse
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()


@router.get("/urls", response_model=URLListResponse)
def get_urls(
    current_user: User = Depends(verify_user_logged_in), db: Session = Depends(get_db)
):
    user_urls = db.query(URL).filter(URL.owner_id == current_user.id).all()
    return {"urls": user_urls}


@router.delete("/urls/{url_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_url(
    url_id: int,
    current_user: User = Depends(verify_user_logged_in),
    db: Session = Depends(get_db),
):
    url = (
        db.query(URL).filter(URL.id == url_id, URL.owner_id == current_user.id).first()
    )
    if url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="URL not found"
        )
    db.delete(url)
    db.commit()
    return {"detail": "URL deleted"}
