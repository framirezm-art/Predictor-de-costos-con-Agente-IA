# Predicción de precios de equipos y materias primas

## Descripción

Implementa un flujo completo para predecir el precio futuro de dos equipos industriales a partir del comportamiento histórico de las materias primas que influyen en su costo. Genera información que posteriormente para ser utilizada por un agente de IA para explicar **por qué** se espera un aumento o disminución del precio de los equipos.

---

# Flujo del análisis

## 1. Análisis exploratorio de datos (EDA)

Inicialmente se realiza una exploración del conjunto de datos para:

* Identificar valores faltantes.
* Obtener estadísticas descriptivas.
* Analizar correlaciones entre materias primas y equipos.
* Comprender qué variables tienen mayor influencia sobre el precio final.

---

## 2. Entrenamiento y comparación de modelos de regresión

Se entrenan múltiples modelos supervisados para estimar el precio de los equipos, entre ellos:

* Regresión Lineal
* Ridge
* Lasso
* XGBoost

Cada modelo es evaluado utilizando métricas de desempeño para seleccionar la alternativa con mejor capacidad predictiva.

Aunque inicialmente se emplea una división aleatoria de entrenamiento, validación y prueba para comparar modelos de forma rápida, posteriormente se reemplaza por una estrategia temporal más adecuada para series de tiempo.

---

## 3. Validación temporal (Walk-Forward Validation)

Una vez identificado el mejor modelo de regresión, el análisis cambia a una validación **walk-forward**. Esta decisión evita el **data leakage temporal**, es decir, que el modelo utilice información del futuro durante el entrenamiento.

---

## 4. Análisis estadístico de las series

Entre las pruebas implementadas se encuentran:

* comparación entre volatilidad histórica y reciente;
* prueba de estacionariedad (ADF);
* identificación automática del orden de diferenciación requerido por ARIMA.

Esto permite seleccionar una configuración apropiada para cada materia prima y evita asumir el mismo comportamiento estadístico para todas las variables.

---

## 5. Pronóstico de materias primas mediante ARIMA

Las materias primas relevantes se pronostican utilizando modelos ARIMA.

La selección del mejor modelo se realiza automáticamente mediante el criterio **AIC (Akaike Information Criterion)**, buscando el equilibrio entre precisión y complejidad.

Cada modelo genera:

* pronóstico esperado;
* error estándar;
* incertidumbre asociada a cada predicción.

---

## 6. Propagación del pronóstico hacia el precio de los equipos

Una vez obtenidos los pronósticos de las materias primas, estos se utilizan como entrada del modelo de regresión previamente validado.

Posteriormente se emplea una simulación Monte Carlo para incorporar la incertidumbre proveniente tanto de:

* los modelos ARIMA,
* como de los errores residuales del modelo de regresión.

Como resultado se obtiene para cada equipo:

* valor esperado;
* intervalo de confianza;
* distribución probable del precio futuro.

Este enfoque proporciona una estimación más robusta que una predicción puntual.

---

# Justificación del horizonte de pronóstico

Se basa en el comportamiento estadístico observado en las series temporales:

* estabilidad de la volatilidad reciente frente a la histórica;
* nivel de incertidumbre del modelo ARIMA;
* capacidad de generalización observada durante la validación temporal.

A medida que aumenta el horizonte de predicción, la incertidumbre crece de forma acumulativa, haciendo que las estimaciones sean menos confiables. Por esta razón se adopta un horizonte moderado, donde aún es posible mantener un equilibrio entre utilidad práctica y confiabilidad estadística.

---

# Variables exportadas para el agente de IA

Al finalizar el notebook se exportan tanto las predicciones de los equipos como las predicciones de las materias primas.

En particular se incluyen:

* pronóstico de **Price_Equipo1**;
* pronóstico de **Price_Equipo2**;
* pronóstico de **Price_Y**;
* pronóstico de **Price_Z**.

Si únicamente se entregara al agente de IA el precio proyectado de los equipos, el modelo podría informar el resultado, pero tendría poca capacidad para explicar el origen del cambio.

Al incluir también las proyecciones de las materias primas, el agente dispone de información suficiente para construir una explicación causal, por ejemplo:

* identificar qué materia prima presenta el mayor incremento esperado;
* relacionar dicho incremento con el aumento proyectado del precio del equipo;
* comparar el comportamiento de distintas materias primas para justificar variaciones moderadas o significativas.

Además, el agente puede complementar esta información mediante herramientas de búsqueda web para consultar noticias económicas, eventos geopolíticos, restricciones de oferta, cambios en la demanda u otros factores externos que expliquen por qué una determinada materia prima aumentó o disminuyó su precio, generando una explicación fundamentada y enriquecida con información actualizada del contexto económico, generando respuestas más útiles para el usuario final.
