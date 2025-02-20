from fastapi import FastAPI
from .database import engine, Base
from router import router

app = FastAPI()
app.include_router(router)

Base.metadata.create_all(bind=engine)
