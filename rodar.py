import os
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
os.chdir(BASE_DIR)

def rodar_pipeline():
    print("\n=== Rodando pipeline de normalização ===\n")
    subprocess.Popen(
        ["python", "scripts/normalizacao/normalizador.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def abrir_dashboard():
    print("\n=== Abrindo dashboard ===\n")
    subprocess.Popen(
        ["python", "ui/dashboard/dashboards.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def sugerir_regras():
    print("\n=== Sugerindo regras com IA ===\n")
    subprocess.Popen(
        ["python", "scripts/sugerir_regras.py"],
        creationflags=subprocess.CREATE_NEW_CONSOLE
    )

def rodar_tudo():
    print("\n=== Rodando tudo ===\n")
    rodar_pipeline()
    sugerir_regras()
    abrir_dashboard()

def menu():
    while True:
        print("\n==============================")
        print("   ORGANIZADOR FINANCEIRO")
        print("==============================")
        print("1 - Rodar pipeline")
        print("2 - Abrir dashboard")
        print("3 - Sugerir regras com IA")
        print("4 - Rodar tudo")
        print("5 - Sair")
        print("==============================")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            rodar_pipeline()
        elif opcao == "2":
            abrir_dashboard()
        elif opcao == "3":
            sugerir_regras()
        elif opcao == "4":
            rodar_tudo()
        elif opcao == "5":
            print("\nSaindo...\n")
            break
        else:
            print("\nOpção inválida. Tente novamente.\n")

if __name__ == "__main__":
    menu()