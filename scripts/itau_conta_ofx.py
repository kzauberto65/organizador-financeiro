import ofxparse
import pandas as pd
from pathlib import Path

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


BASE_DIR = get_project_root()


# ============================================================
# PARSER OFX
# ============================================================

def load_ofx(path: str):
    with open(path, "r", encoding="latin-1") as f:
        return ofxparse.OfxParser.parse(f)


def parse_itau_conta_corrente(ofx, path):
    transactions = []

    for txn in ofx.account.statement.transactions:
        transactions.append({
            "instituicao": "itau",
            "tipo_produto": "conta_corrente",
            "conta_ou_cartao_id": ofx.account.number,
            "origem_arquivo": "ofx",

            # Dados brutos
            "data_lancamento": txn.date,
            "valor": txn.amount,
            "tipo_movimento": "D" if txn.amount < 0 else "R",
            "descricao_original": txn.memo,
            "descricao_normalizada": None,
            "categoria": None,
            "subcategoria": None,

            # Identificação
            "fitid": txn.id,
            "checknum": txn.checknum,

            # Campos universais
            "moeda": "BRL",
            "moeda_original": "BRL",
            "valor_original": txn.amount,
            "cotacao_momento": 1.0,

            # Auxiliares
            "hash_linha": None,
            "arquivo_origem": Path(path).name,
        })

    return pd.DataFrame(transactions)


def save_intermediate(df, output_path: Path):
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output_path, index=False)


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def process_ofx(path: Path):
    ofx = load_ofx(path)
    df = parse_itau_conta_corrente(ofx, path)

    # Caminho correto e robusto
    output_path = BASE_DIR / "intermediario" / "itau" / "conta_corrente.parquet"

    save_intermediate(df, output_path)

    return df