from pathlib import Path
import pandas as pd

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
# FUNÇÕES AUXILIARES
# ============================================================

def extrair(texto, inicio, delimitador):
    pos = texto.find(inicio)
    if pos == -1:
        return ""
    pos += len(inicio)
    fim = texto.find(delimitador, pos)
    return texto[pos:fim].strip()


def parse_ofx_conta(ofx_path):
    with open(ofx_path, "r", encoding="latin-1") as f:
        content = f.read()

    transacoes = []
    blocos = content.split("<STMTTRN>")[1:]  # ignora cabeçalho

    for bloco in blocos:
        try:
            tipo = extrair(bloco, "<TRNTYPE>", "<")
            data = extrair(bloco, "<DTPOSTED>", "<")
            valor = extrair(bloco, "<TRNAMT>", "<")
            memo = extrair(bloco, "<MEMO>", "<")

            data_formatada = pd.to_datetime(data[:8], format="%Y%m%d")

            transacoes.append({
                "data_lancamento": data_formatada,
                "valor": float(valor.replace(",", ".")),
                "descricao_original": memo.strip(),
                "instituicao": "Itau",
                "tipo_produto": "Conta Corrente"
            })
        except Exception:
            continue

    return pd.DataFrame(transacoes)


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def gerar_intermediario_conta():
    # Caminho correto e robusto do OFX
    ofx_path = BASE_DIR / "bruto" / "itau" / "conta" / "ofx" / "seu_arquivo.ofx"

    print("\nLendo arquivo OFX da conta corrente em:", ofx_path)

    if not ofx_path.exists():
        print("❌ Arquivo OFX da conta corrente não encontrado!")
        return None

    df = parse_ofx_conta(ofx_path)

    # Caminho correto para salvar o intermediário
    saida = BASE_DIR / "intermediario" / "itau" / "conta_corrente.parquet"
    saida.parent.mkdir(parents=True, exist_ok=True)

    df.to_parquet(saida, index=False)

    print(f"Intermediário conta corrente gerado com {len(df)} linhas em:", saida)
    return df


if __name__ == "__main__":
    gerar_intermediario_conta()