from dataclasses import dataclass

@dataclass(slots=True)
class Socio:
    nome: str | None = None
    qual: str | None = None
    pais_origem: str | None = None
    nome_rep_legal: str | None = None
    qual_rep_legal: str | None = None