"""Runtime singleton: construye el agente LangGraph una sola vez (costoso) y expone
una función de invocación simple para la capa de aplicación."""
import logging
from functools import lru_cache

from app.exceptions.domain_exceptions import AgentExecutionError
from app.infrastructure.agent.agent_langgraph import build_agent

logger = logging.getLogger("app")


class AgentRuntime:
    def __init__(self):
        self._agent = build_agent()

    def invoke(self, message: str, thread_id: str) -> str:
        """Envía un mensaje al agente manteniendo memoria de conversación por thread_id."""
        config = {"configurable": {"thread_id": thread_id}}
        try:
            result = self._agent.invoke(
                {"messages": [{"role": "user", "content": message}]},
                config=config,
            )
        except Exception as exc:  # noqa: BLE001 - se traduce a error de dominio
            logger.exception("Error invocando el agente LangGraph")
            raise AgentExecutionError(str(exc)) from exc

        final_message = result["messages"][-1]
        return final_message.content


@lru_cache
def get_agent_runtime() -> "AgentRuntime":
    return AgentRuntime()
