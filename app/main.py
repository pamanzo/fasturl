from fastapi import FastAPI
from .database import engine, Base
from .routes import urls

app = FastAPI()
app.include_router(urls.router)

Base.metadata.create_all(bind=engine)
