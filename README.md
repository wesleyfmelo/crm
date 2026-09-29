# Snov.io Corporate Lead Extractor & Enricher 🚀

Ferramenta modular em Python desenvolvida para automação de prospecção B2B, enriquecimento de dados cadastrais de empresas e localização de decisores estratégicos através da API da Snov.io.

---

## 📌 Visão Geral

O projeto automatiza o processo de inteligência de vendas (Sales Intelligence) ao receber nomes de empresas ou domínios e buscar automaticamente os contatos corporativos em departamentos-chave (como **Compras, Jurídico e Finanças**).

### Principais Destaques:
- **Autenticação OAuth 2.0:** Gerenciamento automático de tokens Bearer via `client_credentials`.
- **Resolução Inteligente de Domínios:** Mecanismo de fallback que converte nomes fantasia/razão social em domínios corporativos via API V1/V2.
- **Enriquecimento Resiliente:** Preserva e exporta os dados da empresa mesmo quando nenhum contato for localizado para os filtros informados (preenchendo os campos do funcionário com `"N/A"`).
- **Filtro Avançado de Decisores:** Mapeamento dinâmico por cargos e departamentos.
- **Exportação Formatada:** Geração de relatórios estruturados em Excel (`.xlsx`) prontos para consumo por equipes de SDRs/BDRs ou CRM.

---

## 🗂️️ Estrutura do Projeto

```text
crm/
├── client/              # Cliente HTTP da API Snov.io (OAuth 2.0, Endpoints V1/V2)
│   └── snov_client.py
├── config/              # Variáveis de ambiente e credenciais
│   └── settings.py
├── services/            # Regras de negócio e orquestração da busca
│   └── extractor_service.py
├── utils/               # Exportação e formatação dos relatórios em Excel
│   └── exporter.py
├── .env                 # Arquivo de credenciais locais (não enviado ao Git)
├── .gitignore           # Proteção para venv, .env e arquivos temporários
├── main.py              # Script principal de execução
└── push_git.bat         # Script Batch para automação de Git / GitHub