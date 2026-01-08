import re
from datetime import datetime

path = r"C:\Users\carlo\Organizador Financeiro\financas\bruto\itau\conta\ofx\seu_arquivo.ofx"

with open(path, "r", encoding="latin-1") as f:
    content = f.read()

# Extrai todos os blocos <STMTTRN>...</STMTTRN>
blocks = re.findall(r"<STMTTRN>(.*?)</STMTTRN>", content, re.DOTALL)

print("Total de transações encontradas:", len(blocks))

for b in blocks:
    trntype = re.search(r"<TRNTYPE>(.*)", b).group(1).strip()
    dtposted = re.search(r"<DTPOSTED>(.*)", b).group(1).strip()
    trnamt = re.search(r"<TRNAMT>(.*)", b).group(1).strip()
    memo = re.search(r"<MEMO>(.*)", b).group(1).strip()

    # Converte data
    dt = dtposted[:8]  # YYYYMMDD
    dt = datetime.strptime(dt, "%Y%m%d").date()

    print(f"{dt} | {trnamt} | {trntype} | {memo}")