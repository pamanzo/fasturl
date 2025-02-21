from pydantic import BaseModel, ConfigDict
from datetime import datetime


class URLBase(BaseModel):
    original_url: str
    short_code: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class URLResponse(URLBase):
    id: int


class URLListResponse(BaseModel):
    urls: list[URLResponse]
