from fastapi import APIRouter, Depends

from app.api.deps import get_forecast_service
from app.application.services.forecast_service import ForecastService

router = APIRouter(prefix="/models", tags=["models"])


@router.get("")
def get_all_model_summaries(service: ForecastService = Depends(get_forecast_service)):
    """Coeficientes, R2 y métricas de validación walk-forward de todos los modelos."""
    return service.get_model_summaries()


@router.get("/{equipo}")
def get_model_summary(equipo: str, service: ForecastService = Depends(get_forecast_service)):
    return service.get_model_summary(equipo)


@router.get("/materias-primas/summaries")
def get_raw_material_summaries(service: ForecastService = Depends(get_forecast_service)):
    """Resumen de los modelos ARIMA de materias primas, si fue exportado por el notebook."""
    return service.get_raw_material_summaries()
