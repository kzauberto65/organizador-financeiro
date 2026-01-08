import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]


def carregar_normalizado():
    caminho = BASE_DIR / "normalizado" / "itau" / "conta_corrente.parquet"
    print("Lendo arquivo normalizado:", caminho)
    return pd.read_parquet(caminho)


def preparar_dataframe(df):
    df["data_lancamento"] = pd.to_datetime(df["data_lancamento"])
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
    df = preparar_dataframe(df)

    print("Gerando agregações...")

    mensal = agregacao_mensal(df)
    categoria = agregacao_por_categoria(df)
    subcategoria = agregacao_por_subcategoria(df)

    saida = BASE_DIR / "analises"
    saida.mkdir(exist_ok=True)

    mensal.to_parquet(saida / "mensal.parquet", index=False)
    categoria.to_parquet(saida / "categoria.parquet", index=False)
    subcategoria.to_parquet(saida / "subcategoria.parquet", index=False)

    print("Arquivos gerados em:", saida)