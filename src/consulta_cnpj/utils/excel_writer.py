import pandas as pd
from dataclasses import dataclass
from consulta_cnpj.models.consulta_cnpj_result import ConsultaCNPJResult


@dataclass(slots=True)
class ExcelWriter:
    separador: str = "|"

    def exportar(self, resultados: list[ConsultaCNPJResult], output_path: str) -> None:
        linhas = []

        for r in resultados:
            e = r.empresa

            linha: dict[str, object] = {}

            linha = {
                "Resultado": self._formatar_sucesso(r.sucesso),
                "Erro": self._formatar_erro(r.erro),
                "Cnpj": r.cnpj,
            }

            if not e:
                linhas.append(linha)
                continue

            # Campos simples
            linha.update({
                "Razao Social": e.nome,
                "Fantasia": e.fantasia,
                "Tipo": e.tipo,
                "Porte": e.porte,
                "Natureza Juridica": e.natureza_juridica,
                "Abertura": e.abertura,
                "Ultima Atualizacao": e.ultima_atualizacao,
                "Logradouro": e.logradouro,
                "Numero": e.numero,
                "Complemento": e.complemento,
                "Cep": e.cep,
                "Bairro": e.bairro,
                "Municipio": e.municipio,
                "UF": e.uf,
                "Email": e.email,
                "Telefone": e.telefone,
                "Situacao": e.situacao,
                "Data Situacao": e.data_situacao,
                "Motivo Situacao": e.motivo_situacao,
                "Situacao Especial": e.situacao_especial,
                "Data Situacao Especial": e.data_situacao_especial,
                "Capital Social": self._formatar_moeda(e.capital_social),
                "Efr": self._vazio(e.efr),
                "Simples Optante": self._formatar_bool(e.simples.optante) if e.simples else "",
                "Simples Data Opcao": self._vazio(e.simples.data_opcao) if e.simples else "",
                "Simples Data Exclusao": self._vazio(e.simples.data_exclusao) if e.simples else "",
                "Simei Optante": self._formatar_bool(e.simei.optante) if e.simei else "",
                "Simei Data Opcao": self._vazio(e.simei.data_opcao) if e.simei else "",
                "Simei Data Exclusao": self._vazio(e.simei.data_exclusao) if e.simei else "",
            })

            # Atividades
            linha["Atividade Principal"] = self._concat([
                f"{a.code} - {a.text}" for a in e.atividade_principal
            ])

            linha["Atividades Secundarias"] = self._concat([
                f"{a.code} - {a.text}" for a in e.atividades_secundarias
            ])

            # QSA
            linha["Quadro Societario"] = self._concat([
                self._concat([
                    f"Nome={self._vazio(s.nome)}",
                    f"Qualificacao={self._vazio(s.qual)}",
                    f"Pais={self._vazio(s.pais_origem)}",
                ])
                for s in e.qsa
            ])

            linhas.append(linha)

        df = pd.DataFrame(linhas)
        df.to_excel(output_path, index=False)

    # Helpers
    def _formatar_sucesso(self, sucesso: bool) -> str:
        return "Sucesso" if sucesso else "Falhou"

    def _formatar_bool(self, valor: bool | None) -> str:
        if valor is None:
            return ""
        return "Sim" if valor else "Não"

    def _vazio(self, valor):
        return "" if valor is None else valor

    def _formatar_moeda(self, valor):
        if valor is None:
            return ""

        try:
            return f"{float(valor):,.2f}".replace(",", "").replace(".", ",")
        except Exception:
            return str(valor)

    def _concat(self, items: list[str]) -> str:
        return self.separador.join(
            item for item in items if item
        )

    def _formatar_erro(self, erro: str | None) -> str:
        if not erro:
            return ""

        # melhora mensagens HTTP comuns
        if "400" in erro:
            return "Requisição inválida (CNPJ possivelmente incorreto)"
        if "404" in erro:
            return "CNPJ não encontrado"
        if "429" in erro:
            return "Limite de requisições excedido (3 por minuto)"
        if "500" in erro:
            return "Erro interno na API"
        if "504" in erro:
            return "Timeout na API"

        return erro