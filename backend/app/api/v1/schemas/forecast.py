from pydantic import BaseModel


class EquipoForecastPoint(BaseModel):
    date: str
    p5: float | None = None
    mediana: float | None = None
    p95: float | None = None

    class Config:
        extra = "allow"  # el JSON exportado puede traer columnas adicionales


class RawMaterialForecastPoint(BaseModel):
    date: str
    media: float
    ci_lower: float
    ci_upper: float


class ValidacionWalkForward(BaseModel):
    MAE: float
    RMSE: float
    MAPE_: float | None = None

    class Config:
        extra = "allow"


class ModelSummary(BaseModel):
    features: list[str]
    coeficientes: dict[str, float]
    intercepto: float
    r2_in_sample: float
    validacion_walk_forward: dict
    horizonte_dias: int


class HistoricoPoint(BaseModel):
    date: str
    valor: float
