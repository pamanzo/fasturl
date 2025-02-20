from pydantic import BaseModel
from datetime import datetime


class URLBase(BaseModel):
    original_url: str
    short_code: str
    created_at: datetime

    class Config:
        orm_mode = True


class URLResponse(URLBase):
    id: int


class URLListResponse(BaseModel):
    urls: list[URLResponse]
