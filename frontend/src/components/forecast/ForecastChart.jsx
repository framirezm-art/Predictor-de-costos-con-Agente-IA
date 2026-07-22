import {
  Area,
  CartesianGrid,
  ComposedChart,
  Line,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

/**
 * Grafica un pronóstico con banda de incertidumbre.
 * No asume nombres de columna fijos (el notebook puede exportar
 * "p5/mediana/p95" para equipos o "media/ci_lower/ci_upper" para
 * materias primas, u otros nombres). En vez de eso, detecta
 * automáticamente las columnas numéricas: la de menor promedio es el
 * límite inferior, la de mayor promedio el límite superior, y la
 * restante (o el punto medio) es la línea central.
 */
function detectSeriesKeys(data) {
  const sample = data[0];
  const numericKeys = Object.keys(sample).filter(
    (k) => k !== "date" && typeof sample[k] === "number"
  );

  if (numericKeys.length === 0) return null;

  const withMeans = numericKeys.map((key) => {
    const values = data.map((d) => d[key]).filter((v) => typeof v === "number");
    const mean = values.reduce((a, b) => a + b, 0) / (values.length || 1);
    return { key, mean };
  });
  withMeans.sort((a, b) => a.mean - b.mean);

  const lowerKey = withMeans[0].key;
  const upperKey = withMeans[withMeans.length - 1].key;
  const centerKey =
    withMeans.length >= 3 ? withMeans[Math.floor(withMeans.length / 2)].key : upperKey;

  return { lowerKey, upperKey, centerKey };
}

export default function ForecastChart({ data }) {
  if (!data || data.length === 0) return null;

  const keys = detectSeriesKeys(data);
  if (!keys) return <p className="muted">No se encontraron series numéricas para graficar.</p>;
  const { lowerKey, upperKey, centerKey } = keys;

  return (
    <ResponsiveContainer width="100%" height={340}>
      <ComposedChart data={data} margin={{ top: 10, right: 20, left: 0, bottom: 0 }}>
        <CartesianGrid strokeDasharray="3 3" stroke="var(--border-color)" />
        <XAxis dataKey="date" tick={{ fontSize: 11 }} minTickGap={30} />
        <YAxis domain={["auto", "auto"]} tick={{ fontSize: 11 }} />
        <Tooltip
          contentStyle={{
            background: "var(--surface)",
            border: "1px solid var(--border-color)",
            borderRadius: 8,
          }}
        />
        <Area
          type="monotone"
          dataKey={upperKey}
          stroke="none"
          fill="var(--accent)"
          fillOpacity={0.15}
        />
        <Area
          type="monotone"
          dataKey={lowerKey}
          stroke="none"
          fill="var(--surface)"
          fillOpacity={1}
        />
        <Line
          type="monotone"
          dataKey={centerKey}
          stroke="var(--accent)"
          strokeWidth={2}
          dot={false}
        />
      </ComposedChart>
    </ResponsiveContainer>
  );
}
