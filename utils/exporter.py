import pandas as pd


def export_to_excel(data: list[dict], output_path: str) -> None:
    """Recebe a lista de dados estruturados e exporta para um arquivo Excel (.xlsx)."""
    if not data:
        print("[!] Nenhum dado disponível para exportar.")
        return

    # Converte a lista de dicionários em um DataFrame do Pandas
    df = pd.DataFrame(data)

    # Reordena e renomeia as colunas se necessário, ou exporta diretamente
    df.to_excel(output_path, index=False)
    print(
        f"\n[✔] Relatório exportado com sucesso para o arquivo: '{output_path}'"
    )