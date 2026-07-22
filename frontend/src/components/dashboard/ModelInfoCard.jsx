import Card from "../common/Card";

export default function ModelInfoCard({ equipo, summary }) {
  if (!summary) return null;
  const { features, coeficientes, r2_in_sample, validacion_walk_forward, horizonte_dias } = summary;

  return (
    <Card title={`Modelo: ${equipo}`}>
      <p className="muted">Horizonte: {horizonte_dias} días hábiles</p>
      <p>
        <strong>R² (in-sample):</strong> {r2_in_sample.toFixed(4)}
      </p>
      <p>
        <strong>Variables:</strong> {features.join(", ")}
      </p>
      <ul className="coef-list">
        {Object.entries(coeficientes).map(([k, v]) => (
          <li key={k}>
            {k}: <span className="mono">{v.toFixed(4)}</span>
          </li>
        ))}
      </ul>
      <div className="metrics-grid">
        {Object.entries(validacion_walk_forward).map(([k, v]) => (
          <div key={k} className="metric-pill">
            <span className="metric-label">{k}</span>
            <span className="metric-value">{typeof v === "number" ? v.toFixed(2) : v}</span>
          </div>
        ))}
      </div>
    </Card>
  );
}
