from dataclasses import dataclass, field

from consulta_cnpj.models.atividade import Atividade
from consulta_cnpj.models.socio import Socio
from consulta_cnpj.models.regime_tributario import RegimeTributario


@dataclass(slots=True)
class Empresa:
    cnpj: str | None = None
    nome: str | None = None
    fantasia: str | None = None
    tipo: str | None = None
    porte: str | None = None
    natureza_juridica: str | None = None
    abertura: str | None = None
    ultima_atualizacao: str | None = None

    atividade_principal: list[Atividade] = field(default_factory=list)
    atividades_secundarias: list[Atividade] = field(default_factory=list)

    logradouro: str | None = None
    numero: str | None = None
    complemento: str | None = None
    cep: str | None = None
    bairro: str | None = None
    municipio: str | None = None
    uf: str | None = None

    email: str | None = None
    telefone: str | None = None

    situacao: str | None = None
    data_situacao: str | None = None
    motivo_situacao: str | None = None
    situacao_especial: str | None = None
    data_situacao_especial: str | None = None

    capital_social: str | None = None
    efr: str | None = None

    qsa: list[Socio] = field(default_factory=list)
    
    simples: RegimeTributario | None = None
    simei: RegimeTributario | None = None