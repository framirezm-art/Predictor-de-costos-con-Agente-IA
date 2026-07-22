"""
Acceso al histórico real de precios. Soporta leer directo del CSV (igual que
agent_langgraph.py) o del historico.json exportado por el notebook, lo que esté
disponible, sin duplicar la lógica de negocio que lo consume.
"""
import csv
import json
from functools import lru_cache
from pathlib import Path

RAW_MATERIAL_COLUMNS = ["Price_X", "Price_Y", "Price_Z"]
EQUIPO_COLUMNS = ["Price_Equipo1", "Price_Equipo2"]


class HistoricoRepository:
    def __init__(self, csv_path: Path, json_path: Path | None = None):
        self.csv_path = csv_path
        self.json_path = json_path
        self._rows: list[dict] | None = None

    def _load(self) -> list[dict]:
        if self._rows is not None:
            return self._rows

        if self.csv_path.exists():
            with open(self.csv_path, encoding="utf-8") as f:
                rows = list(csv.DictReader(f))
            for row in rows:
                for col in RAW_MATERIAL_COLUMNS + EQUIPO_COLUMNS:
                    row[col] = float(row[col])
            self._rows = rows
        elif self.json_path and self.json_path.exists():
            with open(self.json_path, encoding="utf-8") as f:
                self._rows = json.load(f)
        else:
            self._rows = []

        return self._rows

    def all_rows(self) -> list[dict]:
        return self._load()

    def range(self, fecha_inicio: str, fecha_fin: str) -> list[dict]:
        return [row for row in self._load() if fecha_inicio <= row["Date"] <= fecha_fin]

    def available_range(self) -> tuple[str, str] | None:
        rows = self._load()
        if not rows:
            return None
        return rows[0]["Date"], rows[-1]["Date"]


@lru_cache
def get_historico_repository() -> "HistoricoRepository":
    from app.core.config import get_settings

    settings = get_settings()
    return HistoricoRepository(
        csv_path=settings.HISTORICO_CSV_PATH,
        json_path=settings.AGENT_DATA_DIR / "historico.json",
    )
