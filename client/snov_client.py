import time
import requests


class SnovClient:

    def __init__(self, client_id: str, client_secret: str):
        self.base_url = "https://api.snov.io"
        self.client_id = client_id
        self.client_secret = client_secret
        self.access_token = self._authenticate()

    def _authenticate(self) -> str:
        """Gera o token Bearer via OAuth2 usando Client Credentials."""
        url = f"{self.base_url}/v1/oauth/access_token"
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }

        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json().get("access_token")

    def _get_headers(self) -> dict:
        """Retorna o cabeçalho padrão com o Bearer Token."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }

    def _get_domain_by_name_v1(self, company_name: str) -> str:
        """Converte o nome da empresa em domínio via V1."""
        url = f"{self.base_url}/v1/get-company-url-by-name"
        payload = {"name": company_name}
        try:
            res = requests.post(
                url, headers=self._get_headers(), json=payload
            )
            if res.status_code == 200:
                data = res.json()
                # Retorna o domínio limpo caso a API devolva URL ou Domain
                domain = data.get("domain") or data.get("url") or ""
                return (
                    domain.replace("https://", "")
                    .replace("http://", "")
                    .replace("www.", "")
                    .strip("/")
                )
        except Exception:
            pass
        return ""

    def fetch_company_data(self, company_name: str) -> dict:
        """Obtém o domínio e dados básicos da empresa."""
        domain = self._get_domain_by_name_v1(company_name)

        # Se não encontrou o domínio pelo nome exato, tenta formatação padrão
        if not domain:
            cleaned_name = (
                company_name.lower().replace(" ", "").replace("-", "")
            )
            domain = f"{cleaned_name}.com.br"

        return {"name": company_name, "domain": domain}

    def fetch_target_contacts(self, domain: str, departments: list[str]) -> list[dict]:
        """Busca os contatos corporativos atrelados ao domínio informado via API V1 oficial (POST)."""
        url = f"{self.base_url}/v1/get-domain-emails-with-info"

        domain_clean = (
            domain.replace("https://", "")
            .replace("http://", "")
            .replace("www.", "")
            .strip("/")
        )

        # O endpoint V1 exige requisição POST com payload no corpo
        payload = {
            "domain": domain_clean,
            "type": "all",
            "limit": 100,
            "offset": 0,
        }

        try:
            # Enviando via POST em formato JSON e com o token de autorização
            res = requests.post(url, headers=self._get_headers(), json=payload)

            # Caso a API exija application/x-www-form-urlencoded em vez de JSON
            if res.status_code == 400:
                res = requests.post(
                    url,
                    headers={
                        "Authorization": f"Bearer {self.access_token}"
                    },
                    data=payload,
                )

            res.raise_for_status()
            data = res.json()

            # A resposta da V1 vem dentro da chave 'emails'
            emails_raw = data.get("emails", [])

            filtered_contacts = []
            for item in emails_raw:
                if not isinstance(item, dict):
                    continue

                dept = item.get("department", "") or ""
                job = (
                    item.get("position", "") or item.get("job_title", "") or ""
                )

                # Se houver lista de departamentos informada, faz o filtro simples
                if departments:
                    matches = any(
                        d.lower() in dept.lower() or d.lower() in job.lower()
                        for d in departments
                    )
                    if not matches:
                        continue

                filtered_contacts.append(
                    {
                        "nome_funcionario": f"{item.get('firstName', '')} {item.get('lastName', '')}".strip(),
                        "cargo": job,
                        "departamento": dept,
                        "email": item.get("email", ""),
                        "status_email": item.get("status", "valid"),
                        "linkedin_pessoal": item.get("social", {}).get(
                            "linkedin", ""
                        )
                        if isinstance(item.get("social"), dict)
                        else "",
                    }
                )

            return filtered_contacts

        except requests.exceptions.RequestException as e:
            print(
                f"  [!] Erro ao buscar contatos para o domínio '{domain_clean}': {e}"
            )
            return []