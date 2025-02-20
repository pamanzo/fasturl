import string
import random
from models import URL
from sqlalchemy.orm import Session


def generate_short_code(length=6):
    return "".join(random.choices(string.ascii_letters + string.digits, k=length))


def verify_code(short_code: str, db: Session):
    return db.query(URL).filter(URL.short_code == short_code).first()
