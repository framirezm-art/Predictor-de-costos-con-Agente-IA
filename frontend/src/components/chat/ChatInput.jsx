import { useState } from "react";

export default function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!text.trim() || disabled) return;
    onSend(text);
    setText("");
  };

  return (
    <form className="chat-input" onSubmit={handleSubmit}>
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Pregunta por el pronóstico de Equipo1, Equipo2..."
        disabled={disabled}
      />
      <button type="submit" className="btn-primary" disabled={disabled}>
        Enviar
      </button>
    </form>
  );
}
