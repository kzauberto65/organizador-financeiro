import json
import hashlib
import pandas as pd
from pathlib import Path
import sys
from datetime import datetime

# ============================
# CONFIGURAÇÃO DE CAMINHOS
# ============================

BASE_DIR = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(BASE_DIR))

from categorizacao.classificador import aplicar_categorizacao


# ============================
# FUNÇÕES AUXILIARES
# ============================

def carregar_regras():
    caminho = BASE_DIR / "config" / "regras_normalizacao.json"
    print("Lendo regras em:", caminho)

    with open(caminho, "r", encoding="utf-8") as f:
        return json.load(f)


def normalizar_descricao(desc):
    return str(desc).lower().strip()


def aplicar_regras(df, regras):
    df["descricao_normalizada"] = df["descricao_original"].apply(normalizar_descricao)
    return df


def gerar_hash(df):
    def hash_linha(row):
        base = f"{row['data_lancamento']}-{row['valor']}-{row['descricao_original']}"
        return hashlib.sha256(base.encode()).hexdigest()

    df["hash_linha"] = df.apply(hash_linha, axis=1)
    return df


def registrar_log(df, caminho_saida):
    log_path = BASE_DIR / "logs" / "execucao_normalizador.log"
    log_path.parent.mkdir(exist_ok=True)

    total = len(df)
    outros = (df["categoria"] == "Outros").sum()
    parcelados = df["parcela_atual"].notna().sum()
    assinaturas = (df["categoria"] == "Assinaturas").sum()
    transf_pf = df["destinatario"].notna().sum()

    with open(log_path, "a", encoding="utf-8") as f:
        f.write(
            f"\n[{datetime.now()}]\n"
            f"Arquivo salvo: {caminho_saida}\n"
            f"Total de linhas: {total}\n"
            f"Outros: {outros}\n"
            f"Parcelamentos detectados: {parcelados}\n"
            f"Assinaturas detectadas: {assinaturas}\n"
            f"Transferências PF detectadas: {transf_pf}\n"
            f"{'-'*40}\n"
        )


# ============================
# PIPELINE PRINCIPAL
# ============================

def normalizar_intermediario(caminho_intermediario, caminho_saida):
    caminho_intermediario = BASE_DIR / caminho_intermediario
    caminho_saida = BASE_DIR / caminho_saida

    # 1. Carrega dados
    df = pd.read_parquet(caminho_intermediario)

    # 2. Normaliza descrição usando JSON
    regras = carregar_regras()
    df = aplicar_regras(df, regras)

    # 3. Aplica categorização nova (classificador inteligente)
    df = aplicar_categorizacao(df)

    # 4. Gera hash
    df = gerar_hash(df)

    # 5. Salva
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(caminho_saida, index=False)

    # 6. Log de execução
    registrar_log(df, caminho_saida)

    print("\nNormalização concluída.")
    print("Arquivo salvo em:", caminho_saida)


# ============================
# EXECUÇÃO DIRETA
# ============================

if __name__ == "__main__":
    normalizar_intermediario(
        "intermediario/itau/conta_corrente.parquet",
        "normalizado/itau/conta_corrente.parquet"
    )