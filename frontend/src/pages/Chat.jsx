import ChatWindow from "../components/chat/ChatWindow";
import ChatInput from "../components/chat/ChatInput";
import { useChat } from "../hooks/useChat";

export default function Chat() {
  const { messages, sendMessage, sending, error } = useChat();

  return (
    <div className="page page-chat">
      <h1>Chat con el agente</h1>
      <p className="muted">
        El agente puede consultar pronósticos, explicar los modelos, revisar histórico y
        buscar contexto de mercado en la web.
      </p>
      <div className="chat-container">
        <ChatWindow messages={messages} sending={sending} error={error} />
        <ChatInput onSend={sendMessage} disabled={sending} />
      </div>
    </div>
  );
}
