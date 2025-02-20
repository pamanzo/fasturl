from datetime import datetime, timezone
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
import string
import random
from ..database import SessionLocal
from ..models import URL, Click

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def generate_short_code(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def verify_code(short_code: str, db: Session = Depends(get_db)):
    return db.query(URL).filter(URL.short_code == short_code).first()


@router.post("/shorten")
def shorten_url(original_url: str, db: Session = Depends(get_db)):
    short_code = generate_short_code()

    while verify_code(short_code) is not None:
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

    if "docs" in str(request.headers.get("referer", "")):
        return {"redirect_to": url_entry.original_url}

    return RedirectResponse(url_entry.original_url)
