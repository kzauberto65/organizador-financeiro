from pathlib import Path
from collections import defaultdict
import re

BASE_DIR = Path(__file__).resolve().parents[1]
LOG_PATH = BASE_DIR / "logs" / "nao_classificados.txt"


# ============================================================
# 1. Carregar descrições não classificadas
# ============================================================

def carregar_descricoes():
    if not LOG_PATH.exists():
        print("Nenhum log encontrado.")
        return []

    with open(LOG_PATH, "r", encoding="utf-8") as f:
        linhas = [l.strip() for l in f.readlines() if l.strip()]
        return list(dict.fromkeys(linhas))  # remove duplicados mantendo ordem


# ============================================================
# 2. Similaridade simples para agrupar descrições parecidas
# ============================================================

def similar(a, b):
    """Retorna True se duas descrições forem parecidas."""
    a = re.sub(r"[^a-z0-9 ]", "", a.lower())
    b = re.sub(r"[^a-z0-9 ]", "", b.lower())

    if a == b:
        return True

    # Se compartilham a primeira palavra → provavelmente são iguais
    if a.split()[0] == b.split()[0]:
        return True

    # Se compartilham 2 palavras → muito provável
    aw = set(a.split())
    bw = set(b.split())
    if len(aw.intersection(bw)) >= 2:
        return True

    return False


def agrupar_similares(descricoes):
    grupos = []
    usados = set()

    for desc in descricoes:
        if desc in usados:
            continue

        grupo = [desc]
        usados.add(desc)

        for outra in descricoes:
            if outra not in usados and similar(desc, outra):
                grupo.append(outra)
                usados.add(outra)

        grupos.append(grupo)

    return grupos


# ============================================================
# 3. Heurística inteligente para sugerir categoria/subcategoria
# ============================================================

def sugerir_regra(desc):
    d = desc.lower()

    # PIX
    if "pix" in d:
        return ("Transferências", "Pix")

    # Transferência PF
    if "transf" in d:
        return ("Transferências", "Pessoa Física")

    # Investimentos
    if "rend" in d or "aplic" in d:
        return ("Investimentos", "Rendimentos")

    # Cartão
    if "itau" in d or "black" in d or "visa" in d or "master" in d:
        return ("Cartão de Crédito", "Fatura")

    # Transporte
    if "autopass" in d or "qrs" in d:
        return ("Transporte", "Mobilidade")

    # Assinaturas
    if any(x in d for x in ["netflix", "spotify", "prime", "google", "apple", "microsoft", "mensal"]):
        return ("Assinaturas", "Serviços Recorrentes")

    return ("Outros", "Sugestão necessária")


# ============================================================
# 4. Gerar blocos de regras prontos para colar
# ============================================================

def gerar_blocos(grupos):
    print("\n=== SUGESTÕES DE REGRAS ===\n")

    for grupo in grupos:
        base = grupo[0]
        cat, sub = sugerir_regra(base)

        print(f"Descrição base: {base}")
        print(f"Grupo: {grupo}")
        print(f"Sugestão: {cat} / {sub}")
        print("Bloco sugerido:")

        palavra_chave = base.split()[0]

        print(f"""{{ 
    "palavras": ["{palavra_chave}"],
    "categoria": "{cat}",
    "subcategoria": "{sub}"
}}""")
        print("-" * 60)


# ============================================================
# 5. Limpar arquivo após sugerir
# ============================================================

def limpar_log():
    if LOG_PATH.exists():
        LOG_PATH.unlink()
        print("\nArquivo nao_classificados.txt limpo.\n")


# ============================================================
# 6. Execução principal
# ============================================================

if __name__ == "__main__":
    descricoes = carregar_descricoes()

    if not descricoes:
        print("Nenhuma descrição para sugerir regras.")
        exit()

    grupos = agrupar_similares(descricoes)
    gerar_blocos(grupos)
    limpar_log()