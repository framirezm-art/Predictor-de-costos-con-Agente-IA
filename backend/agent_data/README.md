# agent_data/

Copia aquí (o monta como volumen) TODOS los archivos que ya generas con el
notebook (sección 6 "Exportar resultados para el agente de IA"):

- forecast_Equipo1.json
- forecast_Equipo2.json
- forecast_Price_Y.json          (alias opcional, ver nota abajo)
- forecast_Z.json / forecast_Price_Z.json  ✅ ya incluido de ejemplo
- forecast_raw_Price_Y.json
- forecast_raw_Price_Z.json
- historico.json
- model_summaries.json           ✅ ya incluido de ejemplo
- raw_material_summaries.json    (opcional, la API lo maneja si no existe)

Además, copia `historico_equipos.csv` en `backend/agent_data/historico_equipos.csv`
(o ajusta `HISTORICO_CSV_PATH` en `.env`).

Estos archivos NO se versionan por defecto en un repo real de producción si
son grandes o si van a regenerarse en cada entrenamiento; aquí se incluyen
para que `docker compose up` funcione end-to-end de inmediato. Si prefieres
no versionarlos, súbelos a Azure Blob Storage y monta el volumen en
App Service, ajustando `AGENT_DATA_DIR`.
