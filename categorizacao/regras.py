# categorizacao/regras.py

# ============================================================
# REGRAS DE CARTÃO (ESPECÍFICAS)
# ============================================================

REGRAS_CARTAO = [
    {
        "palavras": ["itau black", "black 3102", "3102 2450"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Itaú • Mastercard Black"
    },
    {
        "palavras": ["itau platinum"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Itaú • Visa Platinum"
    },
    {
        "palavras": ["nubank"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Nubank • Mastercard Gold"
    },
    {
        "palavras": ["santander unique"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Santander • Visa Infinite"
    }
]

# ============================================================
# ASSINATURAS (PRIORIDADE ALTA)
# ============================================================

REGRAS_ASSINATURAS = [
    {
        "palavras": [
            "netflix", "spotify", "prime video", "disney", "hbo",
            "deezer", "youtube premium", "youtube", "google storage",
            "google play", "icloud", "apple.com/bill", "microsoft",
            "office 365", "adobe", "notion", "canva", "duolingo",
            "recorrente", "assinatura", "mensal", "mensalidade"
        ],
        "categoria": "Assinaturas",
        "subcategoria": "Serviços Recorrentes"
    }
]

# ============================================================
# REGRAS PIX (APENAS PIX REAL)
# ============================================================

REGRAS_PIX = [
    {
        "palavras": ["pix qrs autopass", "autopass"],
        "categoria": "Transporte",
        "subcategoria": "Mobilidade"
    },
    {
        "palavras": ["pix transf"],
        "categoria": "Transferências",
        "subcategoria": "Pix"
    },
    {
        "palavras": ["qms interna"],  # específico
        "categoria": "Transferências",
        "subcategoria": "Pix"
    },
    {
        "palavras": ["confide22"],  # específico
        "categoria": "Transferências",
        "subcategoria": "Pix"
    }
]

# ============================================================
# PARCELAMENTOS (BACKUP TEXTUAL)
# ============================================================

REGRAS_PARCELAMENTO = [
    {
        "palavras": [
            "parc ", "parcela", "parcelado", "parcelamento",
            "1/12", "2/12", "3/12", "4/12", "5/12", "6/12",
            "1 de ", "2 de ", "3 de ", "4 de ", "5 de ", "6 de ",
            "-", " / ", "/ ", " /"
        ],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Parcelado"
    }
]

# ============================================================
# REGRAS GERAIS
# ============================================================

REGRAS_GERAIS = [

    # TRANSPORTE
    {
        "palavras": [
            "uber", "99", "cabify", "mobility", "mobilidade",
            "estapar", "zona azul", "estacionamento", "estac.",
            "shell box", "ipiranga", "posto", "combustivel", "gasolina"
        ],
        "categoria": "Transporte",
        "subcategoria": "Mobilidade"
    },

    # ALIMENTAÇÃO
    {
        "palavras": [
            "ifood", "ubereats", "rappi", "padaria", "restaurante",
            "lanchonete", "bar", "cafeteria", "café", "pizza",
            "burguer", "hamburguer", "sushi", "churrascaria"
        ],
        "categoria": "Alimentação",
        "subcategoria": "Refeições"
    },

    # SUPERMERCADO
    {
        "palavras": [
            "carrefour", "extra", "pao de acucar", "assai", "atacadao",
            "dia%", "mercado", "supermercado", "hortifruti"
        ],
        "categoria": "Alimentação",
        "subcategoria": "Supermercado"
    },

    # RENDA
    {
        "palavras": [
            "salario", "remuneracao salario", "remuneracao",
            "provento", "pagamento", "holerite", "bonus",
            "comissao", "rendimento"
        ],
        "categoria": "Renda",
        "subcategoria": "Salário"
    },

    # SAÚDE
    {
        "palavras": [
            "droga", "drogasil", "droga raia", "farmacia", "remedio",
            "laboratorio", "exame", "clinica", "hospital"
        ],
        "categoria": "Saúde",
        "subcategoria": "Gastos Médicos"
    },

    # LAZER (AGORA SEM ASSINATURAS)
    {
        "palavras": [
            "cinema", "show", "evento", "teatro", "parque", "ingresso"
        ],
        "categoria": "Lazer",
        "subcategoria": "Entretenimento"
    },

    # EDUCAÇÃO
    {
        "palavras": [
            "curso", "faculdade", "universidade", "escola",
            "alura", "udemy", "coursera", "senai", "senac"
        ],
        "categoria": "Educação",
        "subcategoria": "Cursos"
    },

    # CASA
    {
        "palavras": [
            "casas bahia", "magalu", "magazine luiza", "lojas americanas",
            "tokstok", "tok&stok", "mobly", "etna", "construcao",
            "material", "ferramenta", "leroy merlin"
        ],
        "categoria": "Casa",
        "subcategoria": "Manutenção"
    },

    # MORADIA
    {
        "palavras": [
            "aluguel", "condominio", "iptu", "luz", "energia",
            "enel", "copel", "sabesp", "sanepar", "agua"
        ],
        "categoria": "Moradia",
        "subcategoria": "Despesas Fixas"
    },

    # INTERNET / TELEFONIA
    {
        "palavras": [
            "vivo", "claro", "tim", "oi", "internet", "fibra",
            "telefone", "celular", "recarga"
        ],
        "categoria": "Comunicação",
        "subcategoria": "Internet e Telefone"
    },

    # INVESTIMENTOS
    {
        "palavras": [
            "tesouro", "cdb", "lci", "lca", "investimento",
            "xp", "rico", "clear", "nuinvest", "aplicacao",
            "rend pago", "aplic aut", "aplic aut mais"
        ],
        "categoria": "Investimentos",
        "subcategoria": "Aplicações"
    },

    # BANCÁRIOS
    {
        "palavras": [
            "tarifa", "manutencao", "cesta", "juros", "encargos",
            "iof", "taxa"
        ],
        "categoria": "Bancários",
        "subcategoria": "Tarifas"
    },

    # COMPRAS ONLINE
    {
        "palavras": [
            "amazon", "mercado livre", "shopee", "aliexpress",
            "submarino", "fastshop"
        ],
        "categoria": "Compras",
        "subcategoria": "Online"
    },
]

# ============================================================
# FUNÇÃO PRINCIPAL
# ============================================================

def classificar(descricao: str):
    desc = str(descricao).lower()

    # 1. Assinaturas (prioridade máxima)
    for regra in REGRAS_ASSINATURAS:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 2. Cartão
    for regra in REGRAS_CARTAO:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 3. PIX
    for regra in REGRAS_PIX:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 4. Parcelamento textual (backup)
    for regra in REGRAS_PARCELAMENTO:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 5. Regras gerais
    for regra in REGRAS_GERAIS:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 6. Fallback
    return "Outros", "Não classificado"