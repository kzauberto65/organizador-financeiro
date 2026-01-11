import pandas as pd
from pathlib import Path

# ============================================================
# FUNÇÃO DEFINITIVA PARA DETECTAR A RAIZ DO PROJETO
# ============================================================

def get_project_root():
    """
    Retorna a raiz do projeto 'financas' de forma robusta.
    Funciona mesmo se o script for executado:
    - diretamente (python arquivo.py)
    - como módulo (python -m scripts.analise.agregacoes)
    - via .bat
    - via VSCode
    - com cwd diferente
    """
    current = Path(__file__).resolve()

    for parent in current.parents:
        if (parent / "rodar.py").exists():
            return parent

    return current.parents[1]


# BASE_DIR agora é 100% confiável
BASE_DIR = get_project_root()


# ============================================================
# FUNÇÕES DO PIPELINE DE AGREGAÇÕES
# ============================================================

def carregar_normalizado():
    caminho = BASE_DIR / "normalizado" / "itau" / "transacoes.parquet"
    print("Lendo arquivo normalizado:", caminho)

    if not caminho.exists():
        print("❌ Arquivo normalizado não encontrado!")
        return None

    df = pd.read_parquet(caminho)

    if df.empty:
        print("❌ Arquivo normalizado está vazio. Nada a agregar.")
        return None

    return df


def preparar_dataframe(df):
    df["data_lancamento"] = pd.to_datetime(df["data_lancamento"], errors="coerce")
    df = df.dropna(subset=["data_lancamento"])
    df["ano_mes"] = df["data_lancamento"].dt.to_period("M").astype(str)
    return df


def agregacao_mensal(df):
    return (
        df.groupby("ano_mes")["valor"]
        .sum()
        .reset_index()
        .rename(columns={"valor": "total_mes"})
    )


def agregacao_por_categoria(df):
    return (
        df.groupby(["ano_mes", "categoria"])["valor"]
        .sum()
        .reset_index()
        .rename(columns={"valor": "total_categoria"})
    )


def agregacao_por_subcategoria(df):
    return (
        df.groupby(["ano_mes", "categoria", "subcategoria"])["valor"]
        .sum()
        .reset_index()
        .rename(columns={"valor": "total_subcategoria"})
    )


def gerar_agregacoes():
    df = carregar_normalizado()
    if df is None:
        print("⛔ Agregações canceladas.")
        return

    df = preparar_dataframe(df)

    print("Gerando agregações...")

    mensal = agregacao_mensal(df)
    categoria = agregacao_por_categoria(df)
    subcategoria = agregacao_por_subcategoria(df)

    saida = BASE_DIR / "analises"
    saida.mkdir(parents=True, exist_ok=True)

    mensal.to_parquet(saida / "mensal.parquet", index=False)
    categoria.to_parquet(saida / "categoria.parquet", index=False)
    subcategoria.to_parquet(saida / "subcategoria.parquet", index=False)

    print("Arquivos gerados em:", saida)


if __name__ == "__main__":
    gerar_agregacoes()