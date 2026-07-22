import { useCallback, useState } from "react";
import { chatApi } from "../api/chatApi";

/** Maneja el historial de mensajes, el thread_id de memoria, y el estado de envío. */
export function useChat() {
  const [messages, setMessages] = useState([]);
  const [threadId, setThreadId] = useState(null);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState(null);

  const sendMessage = useCallback(
    async (text) => {
      if (!text.trim()) return;
      setError(null);
      setMessages((prev) => [...prev, { role: "user", content: text }]);
      setSending(true);
      try {
        const result = await chatApi.sendMessage(text, threadId);
        setThreadId(result.thread_id);
        setMessages((prev) => [...prev, { role: "agent", content: result.reply }]);
      } catch (err) {
        setError(err.message);
      } finally {
        setSending(false);
      }
    },
    [threadId]
  );

  return { messages, sendMessage, sending, error };
}
