from pathlib import Path
import pandas as pd
from scripts.itau_cartao_visa import parse_itau_visa_csv

# ============================================================
# FUNÇÃO DEFINITIVA PARA DETECTAR A RAIZ DO PROJETO
# ============================================================

def get_project_root():
    """
    Retorna a raiz do projeto 'financas' de forma robusta.
    Funciona mesmo se o script for executado:
    - diretamente
    - como módulo
    - via .bat
    - via VSCode
    - com cwd diferente
    """
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "rodar.py").exists():
            return parent

    return current.parents[1]


# Raiz do projeto
BASE_DIR = get_project_root()


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def gerar_intermediario_visa():
    # Caminho correto e robusto do CSV
    caminho_csv = BASE_DIR / "bruto" / "itau" / "cartoes" / "visa" / "aberta" / "fatura-aberta-202601.csv"

    print("\nLendo arquivo CSV do Visa em:", caminho_csv)

    if not caminho_csv.exists():
        print("❌ Arquivo CSV do Visa não encontrado!")
        return None

    df = parse_itau_visa_csv(caminho_csv)

    # Caminho correto para salvar o intermediário
    saida = BASE_DIR / "intermediario" / "itau" / "cartao_visa.parquet"
    saida.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(saida, index=False)

    print("Intermediário Visa gerado em:", saida)
    return df


if __name__ == "__main__":
    gerar_intermediario_visa()