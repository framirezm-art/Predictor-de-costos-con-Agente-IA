"""Configuración centralizada de la aplicación (12-factor: todo desde variables de entorno)."""
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # --- Metadata ---
    APP_NAME: str = "Cost Forecasting Agent API"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"  # development | production

    # --- CORS ---
    # Lista separada por comas, ej: "https://mi-front.azurestaticapps.net,http://localhost:5173"
    CORS_ORIGINS: str = "http://localhost:5173"

    # --- Agente (NVIDIA API / DeepSeek) ---
    NVIDIA_API_KEY: str = ""
    NVIDIA_MODEL: str = "deepseek-ai/deepseek-v4-flash"
    NVIDIA_BASE_URL: str = "https://integrate.api.nvidia.com/v1"

    # --- Rutas de datos (generadas por el notebook, sección 6) ---
    BASE_DIR: Path = Path(__file__).resolve().parent.parent.parent
    AGENT_DATA_DIR: Path = BASE_DIR / "agent_data"
    HISTORICO_CSV_PATH: Path = BASE_DIR / "agent_data" / "historico_equipos.csv"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [o.strip() for o in self.CORS_ORIGINS.split(",") if o.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
