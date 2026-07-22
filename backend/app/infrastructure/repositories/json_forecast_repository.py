"""
Acceso a los JSON generados por la sección 6 del notebook (agent_data/).
Misma lógica de carga que agent_langgraph.py::load_data, extraída aquí como
repositorio para poder reutilizarla tanto desde el agente como desde los
endpoints REST normales (dashboard, forecast) sin duplicar código.
"""
import json
from functools import lru_cache
from pathlib import Path


class JsonForecastRepository:
    def __init__(self, data_dir: Path):
        self.data_dir = data_dir

    def _read_json(self, filename: str) -> dict | list:
        path = self.data_dir / filename
        with open(path, encoding="utf-8") as f:
            return json.load(f)

    def get_model_summaries(self) -> dict:
        return self._read_json("model_summaries.json")

    def get_raw_material_summaries(self) -> dict:
        path = self.data_dir / "raw_material_summaries.json"
        if not path.exists():
            return {}
        return self._read_json("raw_material_summaries.json")

    def get_equipo_forecast(self, equipo: str) -> list[dict]:
        return self._read_json(f"forecast_{equipo}.json")

    def get_raw_material_forecast(self, materia: str) -> list[dict]:
        return self._read_json(f"forecast_raw_{materia}.json")

    def list_equipos(self) -> list[str]:
        return list(self.get_model_summaries().keys())


@lru_cache
def get_forecast_repository() -> "JsonForecastRepository":
    from app.core.config import get_settings

    return JsonForecastRepository(get_settings().AGENT_DATA_DIR)
