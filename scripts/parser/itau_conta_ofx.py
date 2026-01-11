import re
import pandas as pd
from datetime import datetime
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

def parse_itau_ofx(path):
    with open(path, "r", encoding="latin-1") as f:
        content = f.read()

    blocks = re.findall(r"<STMTTRN>(.*?)</STMTTRN>", content, re.DOTALL)

    rows = []

    for b in blocks:
        trntype = re.search(r"<TRNTYPE>(.*)", b).group(1).strip()
        dtposted = re.search(r"<DTPOSTED>(.*)", b).group(1).strip()
        trnamt = float(re.search(r"<TRNAMT>(.*)", b).group(1).strip())
        memo = re.search(r"<MEMO>(.*)", b).group(1).strip()
        fitid = re.search(r"<FITID>(.*)", b).group(1).strip()

        # Converte data
        dt = datetime.strptime(dtposted[:8], "%Y%m%d").date()

        rows.append({
            "instituicao": "itau",
            "tipo_produto": "conta_corrente",
            "conta_ou_cartao_id": "itau_cc",
            "origem_arquivo": "ofx",

            "data_lancamento": dt,
            "valor": trnamt,
            "tipo_movimento": "D" if trnamt < 0 else "R",
            "descricao_original": memo,
            "descricao_normalizada": None,
            "categoria": None,
            "subcategoria": None,

            "fitid": fitid,
            "moeda": "BRL",
            "valor_original": trnamt,
            "cotacao_momento": 1.0,

            "hash_linha": None,
            "arquivo_origem": Path(path).name,
        })

    return pd.DataFrame(rows)


def save_intermediate(df):
    output = BASE_DIR / "intermediario" / "itau" / "conta_corrente.parquet"
    output.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(output, index=False)
    print("Arquivo salvo em:", output)


def process_itau_ofx(path):
    df = parse_itau_ofx(path)
    save_intermediate(df)
    return df


if __name__ == "__main__":
    caminho = BASE_DIR / "bruto" / "itau" / "conta" / "ofx" / "seu_arquivo.ofx"
    process_itau_ofx(caminho)