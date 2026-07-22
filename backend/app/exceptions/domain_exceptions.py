"""Excepciones de dominio, desacopladas de HTTP. Los routers las traducen a códigos HTTP."""


class DomainError(Exception):
    """Excepción base de dominio."""


class EquipoNotFoundError(DomainError):
    def __init__(self, equipo: str, disponibles: list[str]):
        self.equipo = equipo
        self.disponibles = disponibles
        super().__init__(f"Equipo '{equipo}' no reconocido. Opciones: {disponibles}")


class MateriaPrimaNotFoundError(DomainError):
    def __init__(self, materia: str, disponibles: list[str]):
        self.materia = materia
        self.disponibles = disponibles
        super().__init__(f"Materia prima '{materia}' no reconocida. Opciones: {disponibles}")


class SerieNotFoundError(DomainError):
    def __init__(self, serie: str, disponibles: list[str]):
        self.serie = serie
        self.disponibles = disponibles
        super().__init__(f"Serie '{serie}' no reconocida. Opciones: {disponibles}")


class AgentExecutionError(DomainError):
    """Se lanza cuando la invocación del agente LangGraph falla."""
