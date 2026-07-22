from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="Pregunta del usuario para el agente")
    thread_id: str | None = Field(
        default=None, description="Id de conversación para mantener memoria entre turnos"
    )


class ChatResponse(BaseModel):
    thread_id: str
    reply: str
