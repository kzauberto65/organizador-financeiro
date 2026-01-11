import sys
from pathlib import Path

# Garante que a pasta 'financas' esteja no PYTHONPATH
sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
from categorizacao.classificador import aplicar_categorizacao
from scripts.analise.agregacoes import gerar_agregacoes


def pipeline_itau_conta_parquet(parquet_path):
    BASE_DIR = Path(__file__).resolve().parents[1]  # financas/
    parquet_path = BASE_DIR / parquet_path  # caminho relativo à raiz

    print("========================================")
    print(" INICIANDO PIPELINE DE TESTE (.parquet)")
    print("========================================")
    print("BASE_DIR detectado:", BASE_DIR)
    print("Arquivo recebido:", parquet_path)

    if not parquet_path.exists():
        print(f"❌ Arquivo não encontrado: {parquet_path}")
        return

    print("\n📂 Lendo arquivo PARQUET de teste...")
    df = pd.read_parquet(parquet_path)
    print(f"🔍 Linhas carregadas: {len(df)}")

    print("\n🏷️ Aplicando categorização...")
    df = aplicar_categorizacao(df)

    saida_normalizado = BASE_DIR / "normalizado" / "itau" / "conta_corrente.parquet"
    saida_normalizado.parent.mkdir(parents=True, exist_ok=True)

    print("\n💾 Salvando arquivo categorizado em:")
    print("   ", saida_normalizado)
    df.to_parquet(saida_normalizado, index=False)

    print("\n📊 Gerando agregações para o dashboard...")
    gerar_agregacoes()

    print("\n✅ Pipeline concluído com sucesso!")
    print("👉 Agora abra o dashboard normalmente.")
    print("========================================")


if __name__ == "__main__":
    # Caminho relativo à pasta 'financas'
    caminho_teste = Path("bruto/itau/conta_corrente_teste.parquet")
    pipeline_itau_conta_parquet(caminho_teste)