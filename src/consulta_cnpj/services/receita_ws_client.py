import requests

from consulta_cnpj.models.empresa import Empresa
from consulta_cnpj.models.atividade import Atividade
from consulta_cnpj.models.socio import Socio
from consulta_cnpj.models.regime_tributario import RegimeTributario


class ReceitaWSClient:
    def __init__(self, base_url: str, timeout: int):
        self.base_url = base_url
        self.session = requests.Session()
        self.timeout = timeout


    def consultar_cnpj(self, cnpj: str) -> Empresa:
        url = f"{self.base_url}{cnpj.zfill(14)}"

        response = self.session.get(url, timeout=self.timeout)
        
        if response.status_code != 200:
            raise Exception(f"Erro ao consultar CNPJ: {cnpj} | StatusCode: {response.status_code}")
        
        data = response.json()
        
        if data.get("status") != "OK":
            motivo = data.get('message', 'Motivo não especificado pela API')
            raise Exception(f"CNPJ com status inválido: {cnpj} | Status CNPJ: {data.get('status')} - {motivo}")

        return self._map_to_empresa(data)
    
    
    def _map_to_empresa(self, data: dict) -> Empresa:
        return Empresa(
            cnpj=data.get("cnpj"),
            nome=data.get("nome"),
            fantasia=data.get("fantasia"),
            tipo=data.get("tipo"),
            porte=data.get("porte"),
            natureza_juridica=data.get("natureza_juridica"),
            abertura=data.get("abertura"),
            ultima_atualizacao=data.get("ultima_atualizacao"),

            logradouro=data.get("logradouro"),
            numero=data.get("numero"),
            complemento=data.get("complemento"),
            cep=data.get("cep"),
            bairro=data.get("bairro"),
            municipio=data.get("municipio"),
            uf=data.get("uf"),

            email=data.get("email"),
            telefone=data.get("telefone"),

            situacao=data.get("situacao"),
            data_situacao=data.get("data_situacao"),
            motivo_situacao=data.get("motivo_situacao"),
            situacao_especial=data.get("situacao_especial"),
            data_situacao_especial=data.get("data_situacao_especial"),

            capital_social=data.get("capital_social"),
            efr=data.get("efr"),

            atividade_principal=[
                Atividade(a.get("code"), a.get("text"))
                for a in data.get("atividade_principal") or []
            ],

            atividades_secundarias=[
                Atividade(a.get("code"), a.get("text"))
                for a in data.get("atividades_secundarias") or []
            ],

            qsa=[
                Socio(
                    nome=s.get("nome"),
                    qual=s.get("qual"),
                    pais_origem=s.get("pais_origem"),
                    nome_rep_legal=s.get("nome_rep_legal"),
                    qual_rep_legal=s.get("qual_rep_legal"),
                )
                for s in data.get("qsa") or []
            ],

            simples=None if not data.get("simples") else RegimeTributario(**data["simples"]),
            simei=None if not data.get("simei") else RegimeTributario(**data["simei"]),
        )