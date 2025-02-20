from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
import string
import random
from ..models import URL, Click
from ..database import get_db

router = APIRouter()


def generate_short_code(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def verify_code(short_code: str, db: Session):
    return db.query(URL).filter(URL.short_code == short_code).first()


@router.post("/shorten")
def shorten_url(original_url: str, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    while verify_code(short_code, db) is not None:
        short_code = generate_short_code()

    new_url = URL(original_url=original_url, short_code=short_code)
    db.add(new_url)
    db.commit()
    db.refresh(new_url)
    return {"short_url": f"http://localhost:8000/{short_code}"}


@router.get("/{short_code}", response_model=dict)
def redirect_to_original(
    short_code: str, request: Request, db: Session = Depends(get_db)
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
