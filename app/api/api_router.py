from fastapi import APIRouter
from app.api.routes import upload, auth

api_router = APIRouter()

api_router.include_router(upload.router, prefix="/upload", tags=["upload"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
