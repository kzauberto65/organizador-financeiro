import pandas as pd

# -----------------------------
# PARSER XLS (já existia)
# -----------------------------
def parse_itau_visa_xls(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)

    df = df.rename(columns={
        "Data": "data_lancamento",
        "Descrição": "descricao_original",
        "Valor (R$)": "valor"
    })

    df["data_lancamento"] = pd.to_datetime(df["data_lancamento"], dayfirst=True)
    df["valor"] = df["valor"].astype(float)

    df["instituicao"] = "itau"
    df["tipo_produto"] = "cartao_visa"

    return df


# -----------------------------
# PARSER CSV (REVISADO E ROBUSTO)
# -----------------------------
def parse_itau_visa_csv(caminho_arquivo):

    # Leitura segura com remoção de BOM
    df = pd.read_csv(
        caminho_arquivo,
        sep=",",
        encoding="utf-8-sig"
    )

    # Normaliza nomes das colunas
    df.columns = [
        c.lower()
         .strip()
         .replace("ï»¿", "")
         .replace("\ufeff", "")
        for c in df.columns
    ]

    # Mapeamento flexível
    mapa = {
        "data": "data_lancamento",
        "data compra": "data_lancamento",
        "data da compra": "data_lancamento",

        "lançamento": "descricao_original",
        "lancamento": "descricao_original",
        "descrição": "descricao_original",
        "descricao": "descricao_original",
        "histórico": "descricao_original",
        "historico": "descricao_original",

        "valor": "valor",
        "valor (r$)": "valor",
    }

    # Renomeia apenas colunas existentes
    df = df.rename(columns={orig: mapa[orig] for orig in df.columns if orig in mapa})

    # Validação obrigatória
    obrigatorias = ["data_lancamento", "descricao_original", "valor"]
    for col in obrigatorias:
        if col not in df.columns:
            raise ValueError(f"Coluna obrigatória ausente no CSV: {col}")

    # Converte data (Visa usa YYYY-MM-DD)
    df["data_lancamento"] = pd.to_datetime(
        df["data_lancamento"],
        errors="coerce",
        format="%Y-%m-%d"
    )

    # Converte valor
    df["valor"] = (
        df["valor"]
        .astype(str)
        .str.replace(".", "", regex=False)
        .str.replace(",", ".", regex=False)
        .astype(float)
    )

    df["instituicao"] = "itau"
    df["tipo_produto"] = "cartao_visa"

    return df


# -----------------------------
# NORMALIZAÇÃO (já existia)
# -----------------------------
def normalizar_itau_visa(df):
    df["descricao_normalizada"] = (
        df["descricao_original"]
        .astype(str)
        .str.upper()
        .str.strip()
    )

    df["tipo_movimento"] = df["valor"].apply(
        lambda x: "debito" if x < 0 else "credito"
    )

    df["id_unico"] = df.apply(
        lambda x: hash(f"{x.data_lancamento}-{x.valor}-{x.descricao_original}"),
        axis=1
    )

    return df