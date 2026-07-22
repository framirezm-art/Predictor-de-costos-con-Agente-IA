"""Casos de uso relacionados con pronósticos y resúmenes de modelo."""
from app.exceptions.domain_exceptions import EquipoNotFoundError, MateriaPrimaNotFoundError
from app.infrastructure.repositories.json_forecast_repository import JsonForecastRepository

RAW_MATERIALS_WITH_FORECAST = ["Price_Y", "Price_Z"]


class ForecastService:
    def __init__(self, repo: JsonForecastRepository):
        self.repo = repo

    def list_equipos(self) -> list[str]:
        return self.repo.list_equipos()

    def get_model_summaries(self) -> dict:
        return self.repo.get_model_summaries()

    def get_model_summary(self, equipo: str) -> dict:
        summaries = self.repo.get_model_summaries()
        if equipo not in summaries:
            raise EquipoNotFoundError(equipo, list(summaries.keys()))
        return summaries[equipo]

    def get_equipo_forecast(self, equipo: str) -> list[dict]:
        summaries = self.repo.get_model_summaries()
        if equipo not in summaries:
            raise EquipoNotFoundError(equipo, list(summaries.keys()))
        return self.repo.get_equipo_forecast(equipo)

    def get_raw_material_forecast(self, materia: str) -> list[dict]:
        if materia not in RAW_MATERIALS_WITH_FORECAST:
            raise MateriaPrimaNotFoundError(materia, RAW_MATERIALS_WITH_FORECAST)
        return self.repo.get_raw_material_forecast(materia)

    def get_raw_material_summaries(self) -> dict:
        return self.repo.get_raw_material_summaries()
