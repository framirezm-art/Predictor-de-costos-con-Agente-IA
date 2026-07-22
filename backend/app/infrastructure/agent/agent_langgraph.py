"""
Agente conversacional (LangGraph + DeepSeek-V4-Flash vía NVIDIA API).

NOTA DE REFACTOR (para la prueba técnica / producción):
Este archivo es el `agent_langgraph.py` original, con estos cambios,
estrictamente necesarios para poder reutilizarlo como servicio dentro de FastAPI
en lugar de un script de consola, y para producción:
  1. Las rutas de datos (DATA_DIR / HISTORICO_CSV) ahora vienen de app.core.config
     en vez de estar hardcodeadas como relativas al cwd.
  2. El NVIDIA_API_KEY ya NO está hardcodeado en el código: se lee de la
     configuración/entorno (buena práctica obligatoria antes de subir a un repo
     o desplegar en Azure).
  3. Se eliminó el bucle interactivo `run_agent()` ejecutándose a nivel de
     módulo (si no, se dispararía un `input()` cada vez que FastAPI importa
     el módulo).
  4. La tool `web_search` ya NO usa `DuckDuckGoSearchRun` de `langchain_community`:
     se reemplazó por una tool propia que llama directo a la librería
     `duckduckgo-search`. Motivo: `langchain-community` fue anunciado como
     "sunset" (dejará de mantenerse) por el equipo de LangChain, y arrastraba
     un árbol de dependencias frágil que además chocaba de versión con
     `langgraph`/`langchain-openai` recientes. El comportamiento observable de
     la tool (mismo nombre, misma descripción, mismo tipo de resultado que el
     agente consume) no cambia; solo cambió la implementación interna.

Todo el resto de la lógica (tools de negocio, prompt del sistema, el grafo
`create_react_agent` y el checkpointer de memoria) permanece igual al original.
"""

import json

from duckduckgo_search import DDGS
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

from app.core.config import get_settings
from app.infrastructure.repositories.historico_repository import (
    EQUIPO_COLUMNS,
    RAW_MATERIAL_COLUMNS,
    get_historico_repository,
)
from app.infrastructure.repositories.json_forecast_repository import get_forecast_repository

RAW_MATERIALS_WITH_FORECAST = ["Price_Y", "Price_Z"]  # las que realmente alimentan los modelos

_settings = get_settings()
_forecast_repo = get_forecast_repository()
_historico_repo = get_historico_repository()


def load_data():
    """Misma lógica de carga que el script original, delegando en los repositorios."""
    model_summaries = _forecast_repo.get_model_summaries()

    forecasts = {}
    for equipo in model_summaries:
        forecasts[equipo] = _forecast_repo.get_equipo_forecast(equipo)

    raw_forecasts = {}
    for mat in RAW_MATERIALS_WITH_FORECAST:
        path = _settings.AGENT_DATA_DIR / f"forecast_raw_{mat}.json"
        if path.exists():
            raw_forecasts[mat] = _forecast_repo.get_raw_material_forecast(mat)

    historico = _historico_repo.all_rows()

    return model_summaries, forecasts, raw_forecasts, historico


MODEL_SUMMARIES, FORECASTS, RAW_FORECASTS, HISTORICO = load_data()


# ---------------------------------------------------------------------------
# Herramientas del agente (idénticas al original)
# ---------------------------------------------------------------------------
@tool
def get_equipo_forecast(equipo: str, fecha: str = "") -> str:
    """Obtiene el pronóstico de precio (percentil 5, mediana, percentil 95) de un
    equipo ('Equipo1' o 'Equipo2') para una fecha específica en formato YYYY-MM-DD,
    o para todo el horizonte proyectado si no se da fecha. Úsala siempre que el
    usuario pregunte por un precio futuro."""
    if equipo not in FORECASTS:
        return json.dumps({"error": f"Equipo '{equipo}' no reconocido. Opciones: {list(FORECASTS.keys())}"})

    data = FORECASTS[equipo]
    if not fecha:
        return json.dumps(data, ensure_ascii=False)

    exact = [d for d in data if d["date"] == fecha]
    if exact:
        return json.dumps(exact[0], ensure_ascii=False)

    return json.dumps({
        "aviso": f"No hay pronóstico exacto para {fecha}.",
        "fechas_disponibles": [d["date"] for d in data],
    }, ensure_ascii=False)


@tool
def get_model_info(equipo: str) -> str:
    """Obtiene qué materias primas usa el modelo de un equipo ('Equipo1' o
    'Equipo2'), sus coeficientes, R2 y métricas de error de validación
    walk-forward. Úsala cuando el usuario pregunte por qué el modelo predice
    lo que predice, o qué tan confiable es."""
    if equipo not in MODEL_SUMMARIES:
        return json.dumps({"error": f"Equipo '{equipo}' no reconocido. Opciones: {list(MODEL_SUMMARIES.keys())}"})
    return json.dumps(MODEL_SUMMARIES[equipo], ensure_ascii=False)


@tool
def get_historical_price(serie: str, fecha_inicio: str, fecha_fin: str = "") -> str:
    """Consulta precios HISTÓRICOS reales (ya observados, no proyectados) de una serie:
    'Price_X', 'Price_Y', 'Price_Z', 'Price_Equipo1' o 'Price_Equipo2', entre
    fecha_inicio y fecha_fin (formato YYYY-MM-DD). Si fecha_fin se omite, consulta
    solo fecha_inicio. Si el rango pedido es mayor a 30 días hábiles, devuelve un
    resumen estadístico (min, max, promedio, último valor) en vez de todos los
    valores diarios, para no saturar la respuesta. Úsala para preguntas sobre el
    pasado, tendencias históricas o para comparar el pronóstico contra el histórico."""
    if serie not in RAW_MATERIAL_COLUMNS + EQUIPO_COLUMNS:
        return json.dumps({"error": f"Serie '{serie}' no reconocida. Opciones: {RAW_MATERIAL_COLUMNS + EQUIPO_COLUMNS}"})
    if not HISTORICO:
        return json.dumps({"error": "No se encontró el histórico. Verifica agent_data/historico.json o historico_equipos.csv."})

    fin = fecha_fin or fecha_inicio
    rango = [row for row in HISTORICO if fecha_inicio <= row["Date"] <= fin]
    if not rango:
        fechas = [row["Date"] for row in HISTORICO]
        return json.dumps({
            "aviso": f"No hay datos históricos entre {fecha_inicio} y {fin}.",
            "rango_disponible": {"desde": fechas[0], "hasta": fechas[-1]},
        }, ensure_ascii=False)

    valores = [row[serie] for row in rango]
    if len(rango) > 30:
        return json.dumps({
            "serie": serie, "desde": fecha_inicio, "hasta": fin, "n_dias": len(rango),
            "resumen": {
                "minimo": round(min(valores), 2),
                "maximo": round(max(valores), 2),
                "promedio": round(sum(valores) / len(valores), 2),
                "ultimo_valor": round(valores[-1], 2),
                "ultima_fecha": rango[-1]["Date"],
            },
        }, ensure_ascii=False)

    return json.dumps({
        "serie": serie,
        "valores": [{"date": row["Date"], "valor": row[serie]} for row in rango],
    }, ensure_ascii=False)


@tool
def get_raw_material_forecast(materia: str, fecha: str = "") -> str:
    """Obtiene el pronóstico ARIMA (media e intervalo de confianza 95%) de una
    materia prima: 'Price_Y' o 'Price_Z', para una fecha futura específica
    (YYYY-MM-DD) o para todo el horizonte si no se da fecha. Úsala cuando el
    usuario pregunte por el precio proyectado de las materias primas (no del
    equipo) o quiera entender qué está impulsando el pronóstico del equipo."""
    if materia not in RAW_FORECASTS:
        return json.dumps({
            "error": f"Materia '{materia}' no disponible. Opciones: {list(RAW_FORECASTS.keys())}",
        })

    data = RAW_FORECASTS[materia]
    if not fecha:
        return json.dumps(data, ensure_ascii=False)

    exact = [d for d in data if d["date"] == fecha]
    if exact:
        return json.dumps(exact[0], ensure_ascii=False)

    return json.dumps({
        "aviso": f"No hay pronóstico exacto para {fecha}.",
        "fechas_disponibles": [d["date"] for d in data],
    }, ensure_ascii=False)


@tool
def web_search(query: str) -> str:
    """Busca en la web contexto de mercado actual (noticias de precios de
    commodities, tendencias macro, etc.). Úsala para complementar el
    pronóstico cuantitativo con contexto cualitativo reciente."""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=5))
    except Exception as exc:  # noqa: BLE001 - errores de red/servicio externo
        return json.dumps({"error": f"No se pudo completar la búsqueda web: {exc}"})

    if not results:
        return json.dumps({"aviso": f"No se encontraron resultados para '{query}'."})

    return json.dumps(
        [
            {
                "titulo": r.get("title"),
                "resumen": r.get("body"),
                "url": r.get("href"),
            }
            for r in results
        ],
        ensure_ascii=False,
    )

TOOLS = [
    get_equipo_forecast,
    get_model_info,
    get_historical_price,
    get_raw_material_forecast,
    web_search,
]

SYSTEM_PROMPT = """Eres un asistente analítico para un caso de gestión de costos de equipos
de construcción. Tienes acceso a:
1. Un pronóstico ya calculado (ARIMA + regresión + Monte Carlo) para Equipo1 y Equipo2,
   con intervalos de confianza p5/mediana/p95, horizonte de 40 días hábiles.
2. Información de qué materias primas explican el precio de cada equipo y qué tan
   confiable es cada modelo (validación walk-forward, fuera de muestra real).
3. Histórico real (2010 en adelante) de Price_X, Price_Y, Price_Z, Price_Equipo1 y
   Price_Equipo2, para responder preguntas sobre el pasado o comparar pronóstico vs. histórico.
4. El pronóstico ARIMA (media + IC 95%) de las materias primas Price_Y y Price_Z por
   separado, no solo el precio ya propagado del equipo.
5. Búsqueda web, para traer contexto de mercado actual que complemente el número del modelo.

Cuando respondas sobre precios futuros, siempre usa las herramientas para obtener el
dato real del pronóstico -- nunca inventes cifras. Cuando sea relevante, combina el
número del modelo con contexto de mercado actual vía búsqueda web, dejando claro qué
parte viene del modelo cuantitativo y qué parte es contexto cualitativo externo.
Sé honesto sobre la incertidumbre (usa los rangos p5-p95, no solo la mediana)."""


def build_agent():
    llm = ChatOpenAI(
        model=_settings.NVIDIA_MODEL,
        base_url=_settings.NVIDIA_BASE_URL,
        api_key=_settings.NVIDIA_API_KEY,
        temperature=0.3,
        max_tokens=1500,
        # extra_body es específico de NVIDIA/DeepSeek para el modo de razonamiento
        extra_body={"chat_template_kwargs": {"thinking": True, "reasoning_effort": "high"}},
    )

    checkpointer = MemorySaver()  # memoria de la conversación entre turnos
    agent = create_react_agent(
        llm,
        tools=TOOLS,
        prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    return agent
