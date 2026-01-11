from pathlib import Path
from .regras import classificar
import re
import hashlib

# ============================================================
# FUNÇÃO DEFINITIVA PARA DETECTAR A RAIZ DO PROJETO
# ============================================================

def get_project_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "rodar.py").exists():
            return parent
    return current.parents[1]

BASE_DIR = get_project_root()


# ============================================================
# UTILITÁRIOS
# ============================================================

def gerar_id_parcelamento(descricao):
    """Gera ID estável removendo o trecho X/Y da descrição."""
    desc_limpa = re.sub(r"\b\d{1,2}\s*(/|de|-)\s*\d{1,2}\b", "", descricao)
    base = desc_limpa.strip().lower()
    return hashlib.sha256(base.encode()).hexdigest()[:16]


def eh_nome_pf(texto):
    """Heurística para detectar nomes de pessoas físicas."""
    partes = texto.split()

    if len(partes) < 2:
        return False

    blacklist = {
        "autopass", "qrs", "qms", "internat", "interna",
        "internativ", "autopas", "autopa", "autop",
        "mercado", "google", "apple", "ifood", "rappi",
        "pagamento", "loja", "empresa"
    }

    if any(p.lower() in blacklist for p in partes):
        return False

    return True


def eh_assinatura_oculta(desc):
    """Detecta assinaturas recorrentes mesmo sem palavras-chave."""
    padroes = [
        r"google\s+\d{4}",
        r"apple\s+services",
        r"mercado\s+pago\s+\d{4}",
        r"recorrente",
        r"mensalidade",
    ]
    return any(re.search(p, desc) for p in padroes)


def eh_compra_internacional(desc):
    """Detecta compras internacionais."""
    palavras = [
        "usd", "eur", "gbp", "dolar", "dólar",
        "iof", "compra internacional", "international"
    ]
    return any(p in desc for p in palavras)


def eh_estorno(desc, valor):
    """Detecta estornos automaticamente."""
    return valor > 0 and any(p in desc for p in ["estorno", "reversão", "chargeback"])


# ============================================================
# CLASSIFICADOR PRO
# ============================================================

def aplicar_categorizacao(df, debug=False):

    categorias = []
    subcategorias = []
    parcela_atual_list = []
    parcela_total_list = []
    id_parcelamento_list = []
    destinatarios = []
    nao_classificados = set()

    regex_parcelamento = r"\b(\d{1,2})\s*(/|de|-)\s*(\d{1,2})\b"
    regex_transf_pf = r"(pix\s+transf|transf)\s+([a-zA-ZÀ-ÿ ]{3,})"

    for idx, row in df.iterrows():
        desc = str(row["descricao_normalizada"]).lower()
        valor = float(row.get("valor", 0) or 0)

        # 0. ESTORNOS
        if eh_estorno(desc, valor):
            categorias.append("Ajustes")
            subcategorias.append("Estorno")
            parcela_atual_list.append(None)
            parcela_total_list.append(None)
            id_parcelamento_list.append(None)
            destinatarios.append(None)
            continue

        # 1. ASSINATURAS OCULTAS
        if eh_assinatura_oculta(desc):
            categorias.append("Assinaturas")
            subcategorias.append("Serviços Recorrentes")
            parcela_atual_list.append(None)
            parcela_total_list.append(None)
            id_parcelamento_list.append(None)
            destinatarios.append(None)
            continue

        # 2. PIX > 100
        if desc.startswith("pix") and valor > 100:
            categorias.append("Pix")
            subcategorias.append("Atenção verificar")
            parcela_atual_list.append(None)
            parcela_total_list.append(None)
            id_parcelamento_list.append(None)
            destinatarios.append(None)
            continue

        # 3. PARCELAMENTO REAL
        bloqueia_parc = (
            desc.startswith("pix")
            or desc.startswith("transf")
            or "pix transf" in desc
        )

        match = None if bloqueia_parc else re.search(regex_parcelamento, desc)

        if match and valor < 0:
            atual = int(match.group(1))
            total = int(match.group(3))

            categorias.append("Cartão de Crédito")
            subcategorias.append("Parcelado")
            parcela_atual_list.append(atual)
            parcela_total_list.append(total)
            id_parcelamento_list.append(gerar_id_parcelamento(desc))
            destinatarios.append(None)
            continue

        # 4. TRANSFERÊNCIAS PF
        match_transf = re.search(regex_transf_pf, desc)

        if match_transf and valor < 0:
            nome = match_transf.group(2).strip().title()

            if eh_nome_pf(nome):
                categorias.append("Transferências")
                subcategorias.append("Pessoa Física")
                parcela_atual_list.append(None)
                parcela_total_list.append(None)
                id_parcelamento_list.append(None)
                destinatarios.append(nome)
                continue

        # 5. COMPRAS INTERNACIONAIS
        if eh_compra_internacional(desc):
            categorias.append("Cartão de Crédito")
            subcategorias.append("Compra Internacional")
            parcela_atual_list.append(None)
            parcela_total_list.append(None)
            id_parcelamento_list.append(None)
            destinatarios.append(None)
            continue

        # 6. REGRAS NORMAIS
        cat, sub = classificar(desc)

        categorias.append(cat)
        subcategorias.append(sub)
        parcela_atual_list.append(None)
        parcela_total_list.append(None)
        id_parcelamento_list.append(None)
        destinatarios.append(None)

        if cat == "Outros":
            nao_classificados.add(desc)

    # Atribuição ao DataFrame
    df["categoria"] = categorias
    df["subcategoria"] = subcategorias
    df["parcela_atual"] = parcela_atual_list
    df["parcela_total"] = parcela_total_list
    df["id_parcelamento"] = id_parcelamento_list
    df["destinatario"] = destinatarios

    # LOG
    if nao_classificados:
        log_path = BASE_DIR / "logs" / "nao_classificados.txt"
        log_path.parent.mkdir(exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            for item in sorted(nao_classificados):
                f.write(item + "\n")

    return df