"""Caso de uso: chat con el agente conversacional. No toca la lógica interna del
agente, solo orquesta la llamada y arma la entidad de respuesta."""
import uuid

from app.domain.entities import ChatReply
from app.infrastructure.agent.agent_runtime import AgentRuntime


class ChatService:
    def __init__(self, runtime: AgentRuntime):
        self.runtime = runtime

    def send_message(self, message: str, thread_id: str | None) -> ChatReply:
        tid = thread_id or str(uuid.uuid4())
        reply_text = self.runtime.invoke(message=message, thread_id=tid)
        return ChatReply(thread_id=tid, reply=reply_text)
