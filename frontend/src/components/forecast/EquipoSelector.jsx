export default function EquipoSelector({ equipos, value, onChange }) {
  return (
    <select className="select" value={value} onChange={(e) => onChange(e.target.value)}>
      {equipos.map((eq) => (
        <option key={eq} value={eq}>
          {eq}
        </option>
      ))}
    </select>
  );
}
