from fastapi import APIRouter

from app.api.v1.routers import chat, forecast, health, historico, models

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router)
api_router.include_router(chat.router)
api_router.include_router(forecast.router)
api_router.include_router(models.router)
api_router.include_router(historico.router)
