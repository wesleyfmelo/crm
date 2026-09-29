import os
from pathlib import Path
from dotenv import load_dotenv

# Define o caminho para a raiz do projeto e carrega o arquivo .env
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")

# Leitura das chaves de configuração
SNOV_CLIENT_ID = os.getenv("SNOV_CLIENT_ID")
SNOV_CLIENT_SECRET = os.getenv("SNOV_CLIENT_SECRET")
OUTPUT_EXCEL_PATH = os.getenv("OUTPUT_EXCEL_PATH", "leads_empresas_snov.xlsx")

# Validação para evitar rodar a aplicação sem as credenciais necessárias
if not SNOV_CLIENT_ID or not SNOV_CLIENT_SECRET:
    raise ValueError(
        "Erro: As chaves SNOV_CLIENT_ID e SNOV_CLIENT_SECRET precisam estar preenchidas no arquivo .env!"
    )