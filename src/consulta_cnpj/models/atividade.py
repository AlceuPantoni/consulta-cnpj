from dataclasses import dataclass

@dataclass(slots=True)
class Atividade:
    code: str | None = None
    text: str | None = None