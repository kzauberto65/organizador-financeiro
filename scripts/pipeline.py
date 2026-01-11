from pathlib import Path
import subprocess
import sys

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
# EXECUÇÃO DE SCRIPTS
# ============================================================

def run(script):
    caminho = BASE_DIR / "scripts" / script
    print(f"\n=== Executando {script} ===\n")

    result = subprocess.run([sys.executable, str(caminho)], text=True)

    if result.returncode != 0:
        print(f"❌ Erro ao executar {script}")
    else:
        print(f"✅ {script} concluído com sucesso.")


def rodar_pipeline():
    print("\n==============================")
    print("   PIPELINE COMPLETO ITAÚ")
    print("==============================\n")

    # 1. Conta Corrente
    run("pipeline_itau_conta.py")

    # 2. Cartão Visa
    run("itau_visa_pipeline.py")

    # 3. Normalização
    run("normalizacao/normalizador.py")

    # 4. Agregações
    run("analise/agregacoes.py")

    print("\n==============================")
    print("   PIPELINE FINALIZADO")
    print("==============================\n")


if __name__ == "__main__":
    rodar_pipeline()