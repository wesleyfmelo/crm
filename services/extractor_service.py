from client.snov_client import SnovClient


class CompanyExtractorService:

    DEFAULT_DEPARTMENTS = [
        "Procurement",
        "Purchasing",
        "Supply Chain",
        "Legal",
        "Finance",
        "Accounting",
    ]

    def __init__(self, snov_client: SnovClient):
        self.client = snov_client

    def process_company(self, company_name: str) -> list[dict]:
        """
        Orquestra a busca para uma empresa:
        Retorna os dados da empresa combinados com os contatos (se encontrados),
        ou ao menos o registro cadastral da empresa se nenhum contato for localizado.
        """
        print(f"\n[*] Pesquisando empresa: '{company_name}'...")

        # 1. Obtém os dados da empresa
        raw_company = self.client.fetch_company_data(company_name)

        if not raw_company or not raw_company.get("domain"):
            print(f"[!] Empresa '{company_name}' não foi localizada.")
            return [{
                "empresa_pesquisada": company_name,
                "status_pesquisa": "não_encontrada"
            }]

        domain = raw_company.get("domain")

        # Estrutura base da empresa
        company_info = {
            "empresa_pesquisada": company_name,
            "nome_oficial": raw_company.get("name", company_name),
            "domain": domain,
            "site": f"https://{domain}",
            "ano_fundacao": raw_company.get("founded", ""),
            "setor": raw_company.get("industry", ""),
            "faturamento_medio": raw_company.get("revenue_range", ""),
            "num_funcionarios": raw_company.get("size_range", ""),
            "linkedin_empresa": raw_company.get("linkedin_url", ""),
            "status_pesquisa": "localizada"
        }

        print(f"[+] Empresa localizada: '{company_info['nome_oficial']}' ({domain}).")
        print(f"[*] Buscando contatos no domínio '{domain}'...")

        # 2. Busca os contatos corporativos
        raw_contacts = self.client.fetch_target_contacts(domain, self.DEFAULT_DEPARTMENTS)

        # 3. Se não encontrar contatos, RETORNA OS DADOS DA EMPRESA com campos de contato vazios
        if not raw_contacts:
            print("  └─ Nenhum contato localizado para os filtros informados. Preservando dados da empresa.")
            empty_contact = {
                "nome_funcionario": "N/A",
                "cargo": "N/A",
                "departamento": "N/A",
                "email": "N/A",
                "status_email": "N/A",
                "linkedin_pessoal": "N/A"
            }
            return [{**company_info, **empty_contact}]

        # 4. Se encontrar contatos, combina cada um com os dados da empresa
        records = []
        for c in raw_contacts:
            contact_info = {
                "nome_funcionario": c.get("nome_funcionario", ""),
                "cargo": c.get("cargo", ""),
                "departamento": c.get("departamento", ""),
                "email": c.get("email", ""),
                "status_email": c.get("status_email", ""),
                "linkedin_pessoal": c.get("linkedin_pessoal", "")
            }
            records.append({**company_info, **contact_info})

        print(f"[+] {len(records)} contato(s) associado(s) à empresa com sucesso.")
        return records