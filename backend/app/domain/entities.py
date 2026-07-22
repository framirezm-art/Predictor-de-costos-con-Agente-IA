"""Entidades de dominio, independientes de FastAPI/Pydantic."""
from dataclasses import dataclass


@dataclass(frozen=True)
class ForecastPoint:
    date: str
    p5: float | None = None
    mediana: float | None = None
    p95: float | None = None
    media: float | None = None
    ci_lower: float | None = None
    ci_upper: float | None = None


@dataclass(frozen=True)
class ModelSummary:
    equipo: str
    features: list[str]
    coeficientes: dict[str, float]
    intercepto: float
    r2_in_sample: float
    validacion_walk_forward: dict[str, float]
    horizonte_dias: int


@dataclass(frozen=True)
class ChatReply:
    thread_id: str
    reply: str
