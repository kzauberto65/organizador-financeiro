import json
import hashlib
import pandas as pd
from pathlib import Path
from datetime import datetime

# ============================================================
# FUNÇÃO DEFINITIVA PARA DETECTAR A RAIZ DO PROJETO
# ============================================================

def get_project_root():
    """
    Retorna a raiz do projeto 'financas' de forma robusta.
    Funciona mesmo se o script for executado:
    - diretamente (python arquivo.py)
    - como módulo (python -m scripts.normalizacao.normalizador)
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

# Import do classificador
from categorizacao.classificador import aplicar_categorizacao


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

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


def regras_automaticas(df):
    # 1. Pagamento de fatura
    mask_pag_fatura = df["descricao_normalizada"].str.contains(
        r"(pagamento.*(fatura|cartao|débito automático))|(debito automatico)",
        case=False, na=False
    )
    df.loc[mask_pag_fatura, "categoria"] = "Transferência"
    df.loc[mask_pag_fatura, "subcategoria"] = "Pagamento de Fatura"

    # 2. PIX entre contas próprias
    mask_pix_proprio = df["descricao_normalizada"].str.contains(
        r"(pix.*(próprio|proprio|entre contas|mesma titularidade))",
        case=False, na=False
    )
    df.loc[mask_pix_proprio, "categoria"] = "Transferência"
    df.loc[mask_pix_proprio, "subcategoria"] = "Entre Contas Próprias"

    # 3. Assinaturas
    assinaturas = [
        "netflix", "spotify", "prime", "deezer", "hbo", "max",
        "youtube", "google storage", "icloud", "one drive",
        "chatgpt", "microsoft 365"
    ]
    mask_assinatura = df["descricao_normalizada"].str.contains(
        "|".join(assinaturas), case=False, na=False
    )
    df.loc[mask_assinatura, "categoria"] = "Assinaturas"
    df.loc[mask_assinatura, "subcategoria"] = "Serviços Mensais"

    # 4. Parcelamentos
    mask_parcelado = df["descricao_normalizada"].str.contains(
        r"\d+/\d+", case=False, na=False
    )
    df.loc[mask_parcelado, "categoria"] = "Parcelamentos"
    df.loc[mask_parcelado, "subcategoria"] = "Compra Parcelada"

    # 5. Boletos
    mask_boleto = df["descricao_normalizada"].str.contains(
        r"(boleto|pagamento.*boleto)", case=False, na=False
    )
    df.loc[mask_boleto, "categoria"] = "Pagamentos"
    df.loc[mask_boleto, "subcategoria"] = "Boleto"

    # 6. Saques
    mask_saque = df["descricao_normalizada"].str.contains(
        r"(saque|atm)", case=False, na=False
    )
    df.loc[mask_saque, "categoria"] = "Dinheiro"
    df.loc[mask_saque, "subcategoria"] = "Saque"

    # 7. Estornos
    mask_estorno = (df["valor"] > 0) & df["descricao_normalizada"].str.contains(
        r"(estorno|chargeback|reembolso)", case=False, na=False
    )
    df.loc[mask_estorno, "categoria"] = "Ajustes"
    df.loc[mask_estorno, "subcategoria"] = "Estorno"

    return df


def gerar_hash(df):
    def hash_linha(row):
        base = (
            f"{row['data_lancamento']}-"
            f"{row['valor']}-"
            f"{row['descricao_original']}-"
            f"{row.get('instituicao', '')}-"
            f"{row.get('tipo_produto', '')}"
        )
        return hashlib.sha256(base.encode()).hexdigest()

    df["hash_linha"] = df.apply(hash_linha, axis=1)
    return df


def registrar_log(df, caminho_saida):
    log_path = BASE_DIR / "logs" / "execucao_normalizador.log"
    log_path.parent.mkdir(exist_ok=True)

    total = len(df)
    outros = df.get("categoria", pd.Series()).eq("Outros").sum()
    parcelados = df.get("parcela_atual", pd.Series()).notna().sum()
    assinaturas = df.get("categoria", pd.Series()).eq("Assinaturas").sum()
    transf_pf = df.get("destinatario", pd.Series()).notna().sum()

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


# ============================================================
# PIPELINE PRINCIPAL
# ============================================================

def normalizar_intermediario():
    print("\n=== Carregando intermediários ===")

    dfs = []

    # Caminhos corrigidos e robustos
    conta_path = BASE_DIR / "intermediario/itau/conta_corrente.parquet"
    visa_path  = BASE_DIR / "intermediario/itau/cartao_visa.parquet"

    if conta_path.exists():
        dfs.append(pd.read_parquet(conta_path))

    if visa_path.exists():
        dfs.append(pd.read_parquet(visa_path))

    if not dfs:
        print("Nenhum intermediário encontrado.")
        return

    df = pd.concat(dfs, ignore_index=True)
    print("Total combinado:", len(df))

    df["data_lancamento"] = pd.to_datetime(df["data_lancamento"], errors="coerce")

    regras = carregar_regras()
    df = aplicar_regras(df, regras)
    df = regras_automaticas(df)

    mask_sem_categoria = df["categoria"].isna()
    df.loc[mask_sem_categoria] = aplicar_categorizacao(df[mask_sem_categoria])

    df = gerar_hash(df)
    df = df.sort_values("data_lancamento")

    caminho_saida = BASE_DIR / "normalizado/itau/transacoes.parquet"
    caminho_saida.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(caminho_saida, index=False)

    registrar_log(df, caminho_saida)

    print("\nNormalização concluída.")
    print("Arquivo salvo em:", caminho_saida)


if __name__ == "__main__":
    normalizar_intermediario()