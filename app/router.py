from fastapi import APIRouter

from app.routes.urls import router as urls_router
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router

router = APIRouter()

router.include_router(urls_router)
router.include_router(auth_router)
router.include_router(users_router)
