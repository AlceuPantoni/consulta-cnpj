import time
from typing import Iterator

from consulta_cnpj.services.receita_ws_client import ReceitaWSClient
from consulta_cnpj.models.consulta_cnpj_result import ConsultaCNPJResult


class CnpjProcessorService:
    def __init__(self, client: ReceitaWSClient, delay_seconds: int = 30):
        self.client = client
        self.delay_seconds = delay_seconds

    def processar(self, cnpjs: list[str]) -> Iterator[ConsultaCNPJResult]:
        total = len(cnpjs)

        for i, raw_cnpj in enumerate(cnpjs):
            cnpj = str(raw_cnpj).strip()

            try:
                empresa = self.client.consultar_cnpj(cnpj)

                yield ConsultaCNPJResult(
                    cnpj=cnpj,
                    empresa=empresa,
                    erro=None,
                    sucesso=True
                )

            except Exception as e:
                yield ConsultaCNPJResult(
                    cnpj=cnpj,
                    empresa=None,
                    erro=str(e),
                    sucesso=False
                )

            if i < total - 1:
                time.sleep(self.delay_seconds)