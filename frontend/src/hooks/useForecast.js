import { useCallback, useEffect, useState } from "react";
import { forecastApi } from "../api/forecastApi";

/** Carga el pronóstico de un equipo y expone estado de loading/error uniforme. */
export function useForecast(equipo) {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchData = useCallback(async () => {
    if (!equipo) return;
    setLoading(true);
    setError(null);
    try {
      const result = await forecastApi.getEquipoForecast(equipo);
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, [equipo]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}
