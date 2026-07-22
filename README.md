# Cost Forecast Agent

Aplicación full-stack para explorar el pronóstico de costos de equipos de
construcción: modelos ARIMA + regresión + Monte Carlo, expuestos a través de
un agente conversacional (LangGraph + DeepSeek vía NVIDIA API) y de una API
REST tradicional, con un frontend React para dashboard, gráficos y chat.

## Arquitectura

```
.
├── backend/                     # FastAPI (Clean Architecture)
│   ├── app/
│   │   ├── main.py              # Entry point, wiring de middlewares/routers
│   │   ├── core/                # Configuración (settings vía env vars)
│   │   ├── domain/               # Entidades puras, sin dependencias externas
│   │   ├── application/          # Casos de uso (services) — lógica de negocio
│   │   ├── infrastructure/       # Detalles técnicos: agente LangGraph, repos JSON/CSV
│   │   ├── api/                  # Capa HTTP: routers + schemas Pydantic + DI
│   │   └── exceptions/           # Excepciones de dominio + manejo centralizado
│   ├── agent_data/               # JSON/CSV exportados por el notebook (sección 6)
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/                     # React + Vite
│   ├── src/
│   │   ├── api/                  # Cliente Axios centralizado + servicios por dominio
│   │   ├── hooks/                 # useForecast, useChat (loading/error uniforme)
│   │   ├── components/            # common/, dashboard/, forecast/, chat/
│   │   ├── pages/                 # Dashboard, Forecast, Chat
│   │   └── routes/                # React Router
│   ├── Dockerfile                 # multi-stage build + nginx
│   └── staticwebapp.config.json   # routing SPA para Azure Static Web Apps
├── .github/workflows/             # CI/CD para Azure (backend + frontend)
└── docker-compose.yml
```

### Por qué esta separación

- **`domain/`** no importa nada de FastAPI ni de librerías externas: son las
  reglas de negocio (qué es un `ModelSummary`, un `ChatReply`) que sobreviven
  a cualquier cambio de framework.
- **`application/`** orquesta casos de uso (p.ej. "responder un mensaje del
  chat") usando abstracciones de `domain/`, sin saber si los datos vienen de
  un JSON, una base de datos o una API externa.
- **`infrastructure/`** es donde vive el detalle técnico: cómo se lee el
  `historico_equipos.csv`, cómo se construye el grafo de LangGraph, qué
  modelo LLM se usa. Se puede reemplazar sin tocar `application/`.
- **`api/`** es la capa más externa: solo traduce HTTP <-> casos de uso.

## El agente conversacional

`app/infrastructure/agent/agent_langgraph.py` es una copia casi literal de tu
`agent_langgraph.py` original. Las **modificaciones**, documentadas también en
el propio archivo, fueron:

1. Rutas de datos vía `app.core.config` (antes relativas al cwd).
2. `NVIDIA_API_KEY` leída de variable de entorno (antes hardcodeada).
3. Se eliminó el bucle `run_agent()` a nivel de módulo (si no, se dispararía
   un `input()` al importar el archivo desde FastAPI).
4. La tool `web_search` ya no usa `DuckDuckGoSearchRun` de `langchain_community`
   (paquete anunciado como "sunset" por el equipo de LangChain, y que además
   generaba conflictos de versión con `langgraph`/`langchain-openai` recientes).
   Se reemplazó por una tool propia que llama directo a `duckduckgo-search`,
   con el mismo nombre, misma descripción y mismo tipo de resultado — el
   agente la usa exactamente igual, solo cambió la implementación interna.

Las tools de negocio (`get_equipo_forecast`, `get_model_info`,
`get_historical_price`, `get_raw_material_forecast`), el prompt del sistema,
el grafo (`create_react_agent`) y el checkpointer de memoria **no se
tocaron**.

## Requisitos

- Docker + Docker Compose
- (Para desarrollo local sin Docker) Python 3.11 y Node.js 20 LTS
- Una API key de NVIDIA (`NVIDIA_API_KEY`) para el modelo DeepSeek

## Ejecutar con Docker Compose (recomendado)

```bash
cp .env.example .env
# edita .env y coloca tu NVIDIA_API_KEY real

# Copia tus datos reales del notebook a backend/agent_data/
# (ver backend/agent_data/README.md para el listado completo)
cp /ruta/a/tu/agent_data/*.json backend/agent_data/
cp /ruta/a/tu/historico_equipos.csv backend/agent_data/

docker compose up --build
```

- Backend: http://localhost:8000 (docs interactivos en `/docs`)
- Frontend: http://localhost:5173

## Ejecutar en local sin Docker

**Backend**

```bash
cd backend
python -m venv .venv && source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env  # completa NVIDIA_API_KEY
uvicorn app.main:app --reload --port 8000
```

**Frontend**

```bash
cd frontend
npm install
cp .env.example .env  # ajusta VITE_API_BASE_URL si es necesario
npm run dev
```

## Endpoints principales

| Método | Ruta                                     | Descripción                                   |
|--------|-------------------------------------------|------------------------------------------------|
| POST   | `/api/v1/chat`                            | Envía un mensaje al agente (memoria por `thread_id`) |
| GET    | `/api/v1/forecast/equipos`                | Lista los equipos disponibles                  |
| GET    | `/api/v1/forecast/equipos/{equipo}`       | Pronóstico p5/mediana/p95 de un equipo         |
| GET    | `/api/v1/forecast/materias-primas/{materia}` | Pronóstico ARIMA de una materia prima       |
| GET    | `/api/v1/models`                          | Resumen (coeficientes, R², métricas) de todos los modelos |
| GET    | `/api/v1/models/{equipo}`                 | Resumen de un modelo específico                |
| GET    | `/api/v1/historico`                       | Histórico completo                             |
| GET    | `/api/v1/historico/{serie}?fecha_inicio=&fecha_fin=` | Serie histórica en un rango         |
| GET    | `/api/v1/health`                          | Health check                                   |

## Despliegue en Azure

### Backend → Azure App Service (contenedor)

1. Crea un **Azure Container Registry (ACR)** y un **App Service (Linux, contenedor)**.
2. Configura en GitHub → Settings → Secrets los siguientes valores:
   - `AZURE_ACR_LOGIN_SERVER`, `AZURE_ACR_USERNAME`, `AZURE_ACR_PASSWORD`
   - `AZURE_BACKEND_APP_NAME`
   - `AZURE_BACKEND_PUBLISH_PROFILE` (descárgalo desde el portal de Azure → App Service → "Get publish profile")
3. En App Service → Configuration → Application settings, agrega:
   `NVIDIA_API_KEY`, `NVIDIA_MODEL`, `NVIDIA_BASE_URL`, `CORS_ORIGINS` (con la URL real del frontend).
4. Cada push a `main` que toque `backend/**` dispara
   `.github/workflows/backend-deploy.yml`, que construye la imagen, la sube a
   ACR y la despliega.

### Frontend → Azure Static Web Apps

1. Crea un recurso **Azure Static Web Apps** (plan gratuito o estándar).
2. Copia el token de despliegue a un secret de GitHub:
   `AZURE_STATIC_WEB_APPS_API_TOKEN`.
3. Agrega el secret `VITE_API_BASE_URL` apuntando a la URL pública del
   backend (ej. `https://mi-backend.azurewebsites.net/api/v1`).
4. Cada push a `main` que toque `frontend/**` dispara
   `.github/workflows/frontend-deploy.yml`.

> Alternativa: si prefieres desplegar el frontend también como contenedor en
> App Service en vez de Static Web Apps, usa la imagen generada por
> `frontend/Dockerfile` (nginx) igual que el backend.

## Variables de entorno

Ver `backend/.env.example` y `frontend/.env.example`.

## Buenas prácticas aplicadas

- Tipado con Pydantic (backend) y props explícitas por componente (frontend).
- Manejo centralizado de errores (`app/exceptions/handlers.py` en backend,
  interceptor de Axios en frontend).
- Separación estricta entre presentación (`api/`, `pages/`, `components/`),
  lógica de negocio (`application/`) y acceso a datos (`infrastructure/`).
- Sin credenciales hardcodeadas: todo vía variables de entorno.
- Healthchecks en ambos contenedores para App Service / orquestadores.
