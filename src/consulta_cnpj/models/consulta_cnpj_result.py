from dataclasses import dataclass
from consulta_cnpj.models.empresa import Empresa


@dataclass(slots=True)
class ConsultaCNPJResult:
    cnpj: str
    empresa: Empresa | None
    erro: str | None
    sucesso: bool