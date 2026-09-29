from client.snov_client import SnovClient
from config import settings
from services.extractor_service import CompanyExtractorService
from utils.exporter import export_to_excel

def run():
    print("===================================================")
    print("   SNOV.IO COMPANY & PROSPECT ENRICHER")
    print("===================================================")

    # 1. Inicializa o cliente HTTP com as credenciais lidas do .env
    client = SnovClient(
        client_id=settings.SNOV_CLIENT_ID,
        client_secret=settings.SNOV_CLIENT_SECRET,
    )
    
    # 2. Inicializa o serviço orquestrador
    service = CompanyExtractorService(snov_client=client)
    
    # 3. Defina a lista de empresas que deseja prospectar --> Virá de um excel 
    empresas_alvo = ["Totvs"]
    
    # 4. Executa o pipeline para cada empresa
    resultados_finais = []
    for empresa in empresas_alvo:
        registros = service.process_company(empresa)
        resultados_finais.extend(registros)

    # 5. Exporta o relatório consolidado para Excel
    export_to_excel(resultados_finais, settings.OUTPUT_EXCEL_PATH)
    
if __name__ == "__main__":
    run()