export default function ErrorMessage({ message, onRetry }) {
  if (!message) return null;
  return (
    <div className="error-box">
      <p>⚠️ {message}</p>
      {onRetry && (
        <button onClick={onRetry} className="btn-secondary">
          Reintentar
        </button>
      )}
    </div>
  );
}
