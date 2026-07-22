"""Wiring de dependencias: conecta repositorios (infraestructura) con servicios
(aplicación) para inyectarlos en los routers."""
from functools import lru_cache

from app.application.services.chat_service import ChatService
from app.application.services.forecast_service import ForecastService
from app.application.services.historico_service import HistoricoService
from app.infrastructure.agent.agent_runtime import get_agent_runtime
from app.infrastructure.repositories.historico_repository import get_historico_repository
from app.infrastructure.repositories.json_forecast_repository import get_forecast_repository


@lru_cache
def get_forecast_service() -> ForecastService:
    return ForecastService(get_forecast_repository())


@lru_cache
def get_historico_service() -> HistoricoService:
    return HistoricoService(get_historico_repository())


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService(get_agent_runtime())
