import { axiosClient } from "./axiosClient";

export const forecastApi = {
  listEquipos: () => axiosClient.get("/forecast/equipos").then((r) => r.data),

  getEquipoForecast: (equipo) =>
    axiosClient.get(`/forecast/equipos/${equipo}`).then((r) => r.data),

  getRawMaterialForecast: (materia) =>
    axiosClient.get(`/forecast/materias-primas/${materia}`).then((r) => r.data),

  getModelSummaries: () => axiosClient.get("/models").then((r) => r.data),

  getModelSummary: (equipo) => axiosClient.get(`/models/${equipo}`).then((r) => r.data),

  getFullHistory: () => axiosClient.get("/historico").then((r) => r.data),

  getSeriesRange: (serie, fechaInicio, fechaFin) =>
    axiosClient
      .get(`/historico/${serie}`, { params: { fecha_inicio: fechaInicio, fecha_fin: fechaFin } })
      .then((r) => r.data),
};
