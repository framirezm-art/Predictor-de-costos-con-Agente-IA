import { useEffect, useState } from "react";
import { forecastApi } from "../api/forecastApi";
import Card from "../components/common/Card";
import Loader from "../components/common/Loader";
import ErrorMessage from "../components/common/ErrorMessage";
import ModelInfoCard from "../components/dashboard/ModelInfoCard";

export default function Dashboard() {
  const [summaries, setSummaries] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await forecastApi.getModelSummaries();
      setSummaries(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  if (loading) return <Loader label="Cargando resumen de modelos..." />;
  if (error) return <ErrorMessage message={error} onRetry={load} />;

  return (
    <div className="page">
      <h1>Dashboard</h1>
      <p className="muted">Resumen de los modelos de pronóstico de costos por equipo.</p>
      <div className="grid-cards">
        {Object.entries(summaries || {}).map(([equipo, summary]) => (
          <ModelInfoCard key={equipo} equipo={equipo} summary={summary} />
        ))}
      </div>
      <Card title="Acerca de los modelos" className="mt-lg">
        <p>
          Cada equipo se pronostica combinando ARIMA (para las materias primas) con una
          regresión lineal (para propagar el efecto al precio del equipo) y simulación
          Monte Carlo para estimar el rango de incertidumbre (p5 - mediana - p95) a 40
          días hábiles.
        </p>
      </Card>
    </div>
  );
}
