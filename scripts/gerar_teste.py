import pandas as pd

dados_assinaturas = [
    {
        "descricao_original": "NETFLIX.COM 15/01",
        "descricao_normalizada": "netflix.com",
        "valor": 39.90,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-15"
    },
    {
        "descricao_original": "SPOTIFY PREMIUM 15/01",
        "descricao_normalizada": "spotify premium",
        "valor": 34.90,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-15"
    },
    {
        "descricao_original": "APPLE.COM/BILL 15/01",
        "descricao_normalizada": "apple.com/bill",
        "valor": 9.90,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-15"
    },
    {
        "descricao_original": "MICROSOFT 365 15/01",
        "descricao_normalizada": "microsoft 365",
        "valor": 36.00,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-15"
    }
]

dados_parcelamentos = [
    {
        "descricao_original": "COMPRA LOJA XYZ 1/12",
        "descricao_normalizada": "compra loja xyz 1/12",
        "valor": 120.00,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-10"
    },
    {
        "descricao_original": "COMPRA LOJA XYZ 2/12",
        "descricao_normalizada": "compra loja xyz 2/12",
        "valor": 120.00,
        "tipo_movimento": "D",
        "data_lancamento": "2024-02-10"
    },
    {
        "descricao_original": "COMPRA LOJA ABC 03/10",
        "descricao_normalizada": "compra loja abc 03/10",
        "valor": 89.90,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-12"
    },
    {
        "descricao_original": "COMPRA LOJA ABC 04/10",
        "descricao_normalizada": "compra loja abc 04/10",
        "valor": 89.90,
        "tipo_movimento": "D",
        "data_lancamento": "2024-02-12"
    }
]

dados_transferencias = [
    {
        "descricao_original": "PIX TRANSF MARIA CLARA",
        "descricao_normalizada": "pix transf maria clara",
        "valor": 250.00,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-20"
    },
    {
        "descricao_original": "TRANSF JOAO SILVA",
        "descricao_normalizada": "transf joao silva",
        "valor": 180.00,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-22"
    }
]

dados_gerais = [
    {
        "descricao_original": "UBER VIAGEM 14/01",
        "descricao_normalizada": "uber viagem",
        "valor": 22.50,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-14"
    },
    {
        "descricao_original": "IFOOD PEDIDO 14/01",
        "descricao_normalizada": "ifood pedido",
        "valor": 48.90,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-14"
    },
    {
        "descricao_original": "CARREFOUR 13/01",
        "descricao_normalizada": "carrefour",
        "valor": 189.00,
        "tipo_movimento": "D",
        "data_lancamento": "2024-01-13"
    }
]

df = pd.DataFrame(
    dados_assinaturas +
    dados_parcelamentos +
    dados_transferencias +
    dados_gerais
)

df.to_parquet("conta_corrente_teste.parquet", index=False)

print("Arquivo conta_corrente_teste.parquet gerado com sucesso!")