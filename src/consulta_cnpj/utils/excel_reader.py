import pandas as pd
import re
from dataclasses import dataclass, field


@dataclass(slots=True)
class ExcelReader:
    colunas_validas: list[str] = field(default_factory=lambda: ["CNPJ", "CNPJs", "CNPJ(s)"])

    def ler_cnpjs(self, file_path: str) -> list[str]:
        df = pd.read_excel(file_path, dtype=str)

        df.columns = df.columns.str.strip().str.upper()

        coluna_alvo = None
        for col in self.colunas_validas:
            if col.upper() in df.columns:
                coluna_alvo = col
                break

        if not coluna_alvo:
            nomes_aceitos = ", ".join(self.colunas_validas)
            raise ValueError(
                f"Coluna com CNPJ não encontrada no Excel.\nNomes aceitos: {nomes_aceitos}."
            )

        cnpjs = (
            df[coluna_alvo]
            .dropna()
            .astype(str)
            .tolist()
        )

        return [
            self._normalizar(cnpj)
            for cnpj in cnpjs
            if str(cnpj).strip().lower() != "nan" and str(cnpj).strip()
        ]

    def _normalizar(self, cnpj: str) -> str:
        return re.sub(r"[^a-zA-Z0-9]", "", cnpj).upper()