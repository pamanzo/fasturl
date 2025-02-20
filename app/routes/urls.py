from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from app.auth_logic import verify_user_logged_in
from app.models import URL, Click
from app.database import get_db
from app.utils import generate_short_code, verify_code

router = APIRouter()


@router.post("/shorten")
def shorten_url(
    original_url: str,
    db: Session = Depends(get_db),
    user=Depends(verify_user_logged_in),
):
    short_code = generate_short_code()

    while verify_code(short_code, db) is not None:
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code, owner_id=user.id)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}


@router.get("/{short_code}", response_model=dict)
def redirect_to_original(
    short_code: str,
    request: Request,
    db: Session = Depends(get_db),
    _=Depends(verify_user_logged_in),
):
    url_entry = db.query(URL).filter(URL.short_code == short_code).first()

    if not url_entry:
        raise HTTPException(status_code=404, detail="URL not found")

    user_agent = request.headers.get("user-agent", "Unknown")
    new_click = Click(
        url_id=url_entry.id, user_agent=user_agent, timestamp=datetime.now(timezone.utc)
    )
    db.add(new_click)
    db.commit()

    return {"redirect_to": url_entry.original_url}
