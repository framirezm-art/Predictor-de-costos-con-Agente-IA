from fastapi import APIRouter, Depends

from app.api.deps import get_chat_service
from app.api.v1.schemas.chat import ChatRequest, ChatResponse
from app.application.services.chat_service import ChatService

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
def send_chat_message(
    payload: ChatRequest,
    service: ChatService = Depends(get_chat_service),
):
    """Envía un mensaje al agente conversacional (LangGraph + DeepSeek).
    Reenvía el `thread_id` recibido en la respuesta para mantener memoria
    de conversación en turnos siguientes."""
    result = service.send_message(message=payload.message, thread_id=payload.thread_id)
    return ChatResponse(thread_id=result.thread_id, reply=result.reply)
