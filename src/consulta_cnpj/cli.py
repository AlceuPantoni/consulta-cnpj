import argparse

from consulta_cnpj.config import API_BASE_URL, TIMEOUT, TIME_BETWEEN_REQUESTS
from consulta_cnpj.utils.excel_reader import ExcelReader
from consulta_cnpj.utils.excel_writer import ExcelWriter
from consulta_cnpj.services.receita_ws_client import ReceitaWSClient
from consulta_cnpj.services.cnpj_processor_service import CnpjProcessorService


def run():
    parser = argparse.ArgumentParser(prog="consulta-cnpj")

    parser.add_argument("input", help="Arquivo Excel de entrada")
    parser.add_argument("output", help="Arquivo Excel de saída")

    args = parser.parse_args()

    print("\nConsulta CNPJ iniciado...\n")

    reader = ExcelReader()
    writer = ExcelWriter()

    client = ReceitaWSClient(
        base_url=API_BASE_URL,
        timeout=TIMEOUT
    )

    service = CnpjProcessorService(client, delay_seconds=TIME_BETWEEN_REQUESTS)

    cnpjs = reader.ler_cnpjs(args.input)

    total = len(cnpjs)
    print(f"Iniciando processamento de {total} CNPJs...\n")

    resultados = []

    for index, result in enumerate(service.processar(cnpjs), start=1):
        resultados.append(result)

        print(f"Processado {index} de {total}.")

    writer.exportar(resultados, args.output)

    print("\nProcessamento concluído!")
    print(f"Arquivo '{args.output}' gerado com sucesso!\n")


if __name__ == "__main__":
    run()