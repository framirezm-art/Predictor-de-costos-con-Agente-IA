export default function ChatMessage({ role, content }) {
  const isUser = role === "user";
  return (
    <div className={`chat-message ${isUser ? "chat-message-user" : "chat-message-agent"}`}>
      <span className="chat-message-role">{isUser ? "Tú" : "Agente"}</span>
      <p>{content}</p>
    </div>
  );
}
