"""Manejo centralizado de errores: convierte excepciones de dominio en respuestas HTTP consistentes."""
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.exceptions.domain_exceptions import (
    AgentExecutionError,
    DomainError,
    EquipoNotFoundError,
    MateriaPrimaNotFoundError,
    SerieNotFoundError,
)

logger = logging.getLogger("app")


def _error_body(message: str, detail: dict | None = None) -> dict:
    return {"error": message, "detail": detail or {}}


def register_exception_handlers(app: FastAPI) -> None:
    @app.exception_handler(EquipoNotFoundError)
    async def equipo_not_found_handler(request: Request, exc: EquipoNotFoundError):
        return JSONResponse(status_code=404, content=_error_body(str(exc), {"disponibles": exc.disponibles}))

    @app.exception_handler(MateriaPrimaNotFoundError)
    async def materia_not_found_handler(request: Request, exc: MateriaPrimaNotFoundError):
        return JSONResponse(status_code=404, content=_error_body(str(exc), {"disponibles": exc.disponibles}))

    @app.exception_handler(SerieNotFoundError)
    async def serie_not_found_handler(request: Request, exc: SerieNotFoundError):
        return JSONResponse(status_code=404, content=_error_body(str(exc), {"disponibles": exc.disponibles}))

    @app.exception_handler(AgentExecutionError)
    async def agent_error_handler(request: Request, exc: AgentExecutionError):
        logger.exception("Fallo al invocar el agente")
        return JSONResponse(status_code=502, content=_error_body("El agente conversacional no pudo procesar la solicitud."))

    @app.exception_handler(DomainError)
    async def domain_error_handler(request: Request, exc: DomainError):
        return JSONResponse(status_code=400, content=_error_body(str(exc)))

    @app.exception_handler(Exception)
    async def unhandled_exception_handler(request: Request, exc: Exception):
        logger.exception("Error no controlado")
        return JSONResponse(status_code=500, content=_error_body("Error interno del servidor."))
