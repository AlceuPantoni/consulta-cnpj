import pandas as pd
import re
from dataclasses import dataclass


@dataclass(slots=True)
class ExcelReader:
    coluna_cnpj: str = "CNPJ"

    def ler_cnpjs(self, file_path: str) -> list[str]:
        df = pd.read_excel(file_path, dtype={self.coluna_cnpj: str})

        if self.coluna_cnpj not in df.columns:
            raise ValueError(
                f"Coluna '{self.coluna_cnpj}' não encontrada no Excel."
            )

        cnpjs = (
            df[self.coluna_cnpj]
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