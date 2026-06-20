from dataclasses import dataclass

@dataclass(slots=True)
class RegimeTributario:
    optante: bool
    data_opcao: str | None = None
    data_exclusao: str | None = None
    ultima_atualizacao: str | None = None