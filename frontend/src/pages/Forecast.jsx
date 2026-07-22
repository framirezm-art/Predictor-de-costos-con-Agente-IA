import { useEffect, useState } from "react";
import { forecastApi } from "../api/forecastApi";
import { useForecast } from "../hooks/useForecast";
import Card from "../components/common/Card";
import Loader from "../components/common/Loader";
import ErrorMessage from "../components/common/ErrorMessage";
import EquipoSelector from "../components/forecast/EquipoSelector";
import ForecastChart from "../components/forecast/ForecastChart";

export default function Forecast() {
  const [equipos, setEquipos] = useState([]);
  const [selected, setSelected] = useState(null);
  const { data, loading, error, refetch } = useForecast(selected);

  useEffect(() => {
    forecastApi
      .listEquipos()
      .then((res) => {
        setEquipos(res.equipos);
        setSelected(res.equipos[0] ?? null);
      })
      .catch(() => {});
  }, []);

  return (
    <div className="page">
      <div className="page-header">
        <h1>Pronóstico</h1>
        {equipos.length > 0 && (
          <EquipoSelector equipos={equipos} value={selected} onChange={setSelected} />
        )}
      </div>

      <Card title={selected ? `Proyección — ${selected}` : "Proyección"}>
        {loading && <Loader label="Cargando pronóstico..." />}
        {error && <ErrorMessage message={error} onRetry={refetch} />}
        {!loading && !error && <ForecastChart data={data} />}
      </Card>
    </div>
  );
}
