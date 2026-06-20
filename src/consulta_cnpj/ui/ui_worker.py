from pathlib import Path
from PySide6.QtCore import QThread, Signal

from consulta_cnpj.config import API_BASE_URL, TIMEOUT, TIME_BETWEEN_REQUESTS
from consulta_cnpj.services.receita_ws_client import ReceitaWSClient
from consulta_cnpj.services.cnpj_processor_service import CnpjProcessorService
from consulta_cnpj.utils.excel_writer import ExcelWriter

class CnpjWorker(QThread):
    progress_updated = Signal(int)
    status_updated = Signal(str)
    log_updated = Signal(str)
    finished_success = Signal(str)
    finished_cancelled = Signal() 

    def __init__(self, cnpjs, input_file):
        super().__init__()
        self.cnpjs = cnpjs
        self.input_file = input_file
        self.is_cancelled = False

    def run(self):
        client = ReceitaWSClient(
            base_url=API_BASE_URL,
            timeout=TIMEOUT
        )
        service = CnpjProcessorService(client, delay_seconds=TIME_BETWEEN_REQUESTS)
        writer = ExcelWriter()

        total = len(self.cnpjs)
        resultados = []

        for i, result in enumerate(service.processar(self.cnpjs), start=1):
            if self.is_cancelled:
                self.log_updated.emit("⚠️ Processamento cancelado pelo usuário.")
                self.finished_cancelled.emit() 
                return

            resultados.append(result)

            percent = int((i / total) * 100)
            self.progress_updated.emit(percent)
            self.status_updated.emit(f"{i} / {total}")
            self.log_updated.emit(f"Processado {i} de {total} CNPJs.")

        output_path = str(
            Path(self.input_file).with_name(
                Path(self.input_file).stem + "_RESULTADO.xlsx"
            )
        )

        writer.exportar(resultados, output_path)
        self.finished_success.emit(output_path)