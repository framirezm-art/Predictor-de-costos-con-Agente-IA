import { useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import Loader from "../common/Loader";
import ErrorMessage from "../common/ErrorMessage";

export default function ChatWindow({ messages, sending, error }) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, sending]);

  return (
    <div className="chat-window">
      {messages.length === 0 && (
        <p className="muted">
          Pregúntale al agente por el pronóstico de un equipo, el porqué del modelo, o
          compáralo con el histórico.
        </p>
      )}
      {messages.map((m, i) => (
        <ChatMessage key={i} role={m.role} content={m.content} />
      ))}
      {sending && <Loader label="El agente está pensando..." />}
      <ErrorMessage message={error} />
      <div ref={bottomRef} />
    </div>
  );
}
