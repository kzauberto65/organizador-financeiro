from pathlib import Path
from .regras import classificar
import re
import hashlib

BASE_DIR = Path(__file__).resolve().parents[1]


def gerar_id_parcelamento(descricao):
    base = descricao.strip().lower()
    return hashlib.sha256(base.encode()).hexdigest()[:16]


def aplicar_categorizacao(df):
    print("\n==============================")
    print(">> DEBUG: Classificador carregado")
    print(">> Caminho:", Path(__file__).resolve())
    print("==============================\n")

    categorias = []
    subcategorias = []
    parcela_atual_list = []
    parcela_total_list = []
    id_parcelamento_list = []
    destinatarios = []
    nao_classificados = set()

    # Regex mais robusta para parcelamento
    regex_parcelamento = r"\b(\d{1,2})\s*(/|de|-)\s*(\d{1,2})\b"

    # Regex robusta para transferência PF
    regex_transf_pf = r"(pix\s+transf|transf)\s+([a-zA-ZÀ-ÿ ]+)"

    for idx, row in df.iterrows():
        desc = str(row["descricao_normalizada"]).lower()
        valor = float(row.get("valor", 0) or 0)

        print(f"\n[DEBUG] Processando linha {idx}: '{desc}' (valor={valor})")

        # ============================================================
        # 1. PIX > 100
        # ============================================================
        if desc.startswith("pix") and valor > 100:
            print("  -> Regra PIX > 100 aplicada")
            categorias.append("Pix")
            subcategorias.append("Atenção verificar")
            parcela_atual_list.append(None)
            parcela_total_list.append(None)
            id_parcelamento_list.append(None)
            destinatarios.append(None)
            continue

        # ============================================================
        # 2. PARCELAMENTO REAL (regex robusta)
        # ============================================================
        bloqueia_parc = (
            desc.startswith("pix")
            or desc.startswith("transf")
            or "pix transf" in desc
        )

        if bloqueia_parc:
            print("  -> Parcelamento BLOQUEADO (PIX/TRANSF no início)")
            match = None
        else:
            match = re.search(regex_parcelamento, desc)
            if match:
                atual = int(match.group(1))
                total = int(match.group(3))
                print(f"  -> Parcelamento detectado: {atual}/{total}")

                categorias.append("Cartão de Crédito")
                subcategorias.append("Parcelado")
                parcela_atual_list.append(atual)
                parcela_total_list.append(total)
                id_parcelamento_list.append(gerar_id_parcelamento(desc))
                destinatarios.append(None)
                continue

        # ============================================================
        # 3. TRANSFERÊNCIAS PARA PESSOAS (nome composto)
        # ============================================================
        match_transf = re.search(regex_transf_pf, desc)

        if match_transf:
            nome = match_transf.group(2).strip().title()
            print(f"  -> Possível transferência detectada para '{nome}'")

            blacklist = [
                "autopass", "qrs", "qms", "internat", "interna",
                "internativ", "autopas", "autopa", "autop"
            ]

            if nome.lower() not in blacklist:
                print("     -> Nome válido. Classificando como Transferência PF.")
                categorias.append("Transferências")
                subcategorias.append("Pessoa Física")
                parcela_atual_list.append(None)
                parcela_total_list.append(None)
                id_parcelamento_list.append(None)
                destinatarios.append(nome)
                continue
            else:
                print("     -> Nome inválido (blacklist). Ignorando regra PF.")

        # ============================================================
        # 4. REGRAS NORMAIS
        # ============================================================
        print("  -> Aplicando regras normais...")
        cat, sub = classificar(desc)
        print(f"     -> Resultado regras: {cat} / {sub}")

        categorias.append(cat)
        subcategorias.append(sub)
        parcela_atual_list.append(None)
        parcela_total_list.append(None)
        id_parcelamento_list.append(None)
        destinatarios.append(None)

        if cat == "Outros":
            print("     -> Adicionado ao log de não classificados")
            nao_classificados.add(desc)

    # ============================================================
    # Atribuição ao DataFrame
    # ============================================================
    print("\n[DEBUG] Finalizando categorização e atribuindo colunas ao DataFrame...")
    df["categoria"] = categorias
    df["subcategoria"] = subcategorias
    df["parcela_atual"] = parcela_atual_list
    df["parcela_total"] = parcela_total_list
    df["id_parcelamento"] = id_parcelamento_list
    df["destinatario"] = destinatarios

    # ============================================================
    # LOG
    # ============================================================
    if nao_classificados:
        print(f"[DEBUG] {len(nao_classificados)} itens adicionados ao log de não classificados")
        log_path = BASE_DIR / "logs" / "nao_classificados.txt"
        log_path.parent.mkdir(exist_ok=True)
        with open(log_path, "a", encoding="utf-8") as f:
            for item in sorted(nao_classificados):
                f.write(item + "\n")

    print("\n>> DEBUG: Categorização concluída com sucesso!\n")
    return df