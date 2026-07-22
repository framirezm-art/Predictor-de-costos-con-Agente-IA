from fastapi import APIRouter, Depends

from app.api.deps import get_forecast_service
from app.application.services.forecast_service import ForecastService

router = APIRouter(prefix="/forecast", tags=["forecast"])


@router.get("/equipos")
def list_equipos(service: ForecastService = Depends(get_forecast_service)):
    """Lista los equipos disponibles (ej. Equipo1, Equipo2)."""
    return {"equipos": service.list_equipos()}


@router.get("/equipos/{equipo}")
def get_equipo_forecast(equipo: str, service: ForecastService = Depends(get_forecast_service)):
    """Pronóstico (p5 / mediana / p95) de un equipo para el horizonte completo."""
    return service.get_equipo_forecast(equipo)


@router.get("/materias-primas/{materia}")
def get_raw_material_forecast(materia: str, service: ForecastService = Depends(get_forecast_service)):
    """Pronóstico ARIMA (media + IC 95%) de una materia prima (Price_Y, Price_Z)."""
    return service.get_raw_material_forecast(materia)
