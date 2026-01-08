from parser.itau_conta_ofx import process_itau_ofx
from normalizacao.normalizador import normalizar_intermediario


def pipeline_itau_conta(ofx_path):
    print("📂 Lendo arquivo OFX...")
    process_itau_ofx(ofx_path)

    print("🔄 Normalizando dados...")
    normalizar_intermediario(
        "financas/intermediario/itau/conta_corrente.parquet",
        "financas/normalizado/itau/conta_corrente.parquet"
    )


if __name__ == "__main__":
    caminho = r"C:\Users\carlo\Organizador Financeiro\financas\bruto\itau\conta\ofx\seu_arquivo.ofx"
    pipeline_itau_conta(caminho)