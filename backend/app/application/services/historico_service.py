"""Casos de uso relacionados con el histórico real de precios."""
from app.exceptions.domain_exceptions import SerieNotFoundError
from app.infrastructure.repositories.historico_repository import (
    EQUIPO_COLUMNS,
    RAW_MATERIAL_COLUMNS,
    HistoricoRepository,
)

VALID_SERIES = RAW_MATERIAL_COLUMNS + EQUIPO_COLUMNS


class HistoricoService:
    def __init__(self, repo: HistoricoRepository):
        self.repo = repo

    def get_full_history(self) -> list[dict]:
        return self.repo.all_rows()

    def get_series_range(self, serie: str, fecha_inicio: str, fecha_fin: str | None = None) -> list[dict]:
        if serie not in VALID_SERIES:
            raise SerieNotFoundError(serie, VALID_SERIES)

        fin = fecha_fin or fecha_inicio
        rango = self.repo.range(fecha_inicio, fin)
        return [{"date": row["Date"], "valor": row[serie]} for row in rango]
