from fastapi import APIRouter, Depends, Query

from app.api.deps import get_historico_service
from app.application.services.historico_service import HistoricoService

router = APIRouter(prefix="/historico", tags=["historico"])


@router.get("")
def get_full_history(service: HistoricoService = Depends(get_historico_service)):
    """Histórico completo (2010 en adelante) de todas las series."""
    return service.get_full_history()


@router.get("/{serie}")
def get_series_range(
    serie: str,
    fecha_inicio: str = Query(..., description="YYYY-MM-DD"),
    fecha_fin: str | None = Query(default=None, description="YYYY-MM-DD"),
    service: HistoricoService = Depends(get_historico_service),
):
    """Serie histórica (Price_X, Price_Y, Price_Z, Price_Equipo1, Price_Equipo2) en un rango de fechas."""
    return service.get_series_range(serie, fecha_inicio, fecha_fin)
