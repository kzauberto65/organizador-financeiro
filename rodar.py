import subprocess
from pathlib import Path


# ============================================================
# FUNÇÃO DEFINITIVA PARA DETECTAR A RAIZ DO PROJETO
# ============================================================

def get_project_root():
    """
    Retorna a raiz do projeto 'financas' de forma robusta.
    Funciona mesmo se o script for executado:
    - diretamente (python rodar.py)
    - como módulo (python -m scripts.x)
    - via .bat
    - via VSCode
    - com cwd diferente
    """
    current = Path(__file__).resolve()

    # Sobe a árvore até encontrar o arquivo que define a raiz do projeto
    for parent in current.parents:
        if (parent / "rodar.py").exists():
            return parent

    # fallback seguro
    return current.parent


# BASE_DIR agora é 100% confiável
BASE_DIR = get_project_root()
print("RODAR EXECUTADO:", __file__)
print("USANDO ESTE RODAR:", __file__)


# ============================================================
# FUNÇÕES DO PIPELINE
# ============================================================

def gerar_intermediarios():
    print("\n=== Gerando intermediários ===\n")

    subprocess.run(
        ["python", "-m", "scripts.pipeline_itau_conta"],
        text=True,
        cwd=BASE_DIR
    )

    subprocess.run(
        ["python", "-m", "scripts.itau_visa_pipeline"],
        text=True,
        cwd=BASE_DIR
    )

    print("\n=== Intermediários gerados ===\n")


def rodar_pipeline():
    print("\n=== Rodando pipeline de normalização ===\n")

    subprocess.run(
        ["python", "-m", "scripts.normalizacao.normalizador"],
        text=True,
        cwd=BASE_DIR
    )

    print("\n=== Gerando agregações ===\n")

    subprocess.run(
        ["python", "-m", "scripts.analise.agregacoes"],
        text=True,
        cwd=BASE_DIR
    )

    print("\n=== Pipeline finalizado ===\n")


def abrir_dashboard():
    print("\n=== Abrindo dashboard ===\n")

    caminho = BASE_DIR / "ui" / "dashboard" / "dashboard.py"

    subprocess.run(
        ["python", str(caminho)],
        text=True,
        cwd=BASE_DIR
    )

def rodar_tudo():
    print("\n=== Rodando tudo ===\n")
    gerar_intermediarios()
    rodar_pipeline()
    abrir_dashboard()


# ============================================================
# MENU
# ============================================================

def menu():
    while True:
        print("\n=== MENU DO ORGANIZADOR FINANCEIRO ===")
        print("1 - Rodar pipeline (normalização + análises)")
        print("2 - Abrir dashboard")
        print("3 - Rodar tudo")
        print("4 - Gerar intermediários (Conta + Visa)")
        print("5 - Sair")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            rodar_pipeline()

        elif opcao == "2":
            abrir_dashboard()

        elif opcao == "3":
            rodar_tudo()

        elif opcao == "4":
            gerar_intermediarios()

        elif opcao == "5":
            print("Saindo...")
            break

        else:
            print("Opção inválida. Tente novamente.")


if __name__ == "__main__":
    menu()