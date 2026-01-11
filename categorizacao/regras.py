# categorizacao/regras.py

# ============================================================
# ASSINATURAS (PRIORIDADE MÁXIMA)
# ============================================================

REGRAS_ASSINATURAS = [
    {
        "palavras": [
            # Streaming
            "netflix", "spotify", "prime video", "primevideo", "amzn prime",
            "disney", "hbo", "max", "globoplay",

            # Serviços digitais
            "deezer", "youtube premium", "youtube music", "google storage",
            "google play", "google *youtube", "icloud", "apple.com/bill",
            "apple services", "microsoft 365", "office 365", "adobe",
            "notion", "canva", "duolingo",

            # Indicadores de recorrência
            "recorrente", "assinatura", "mensalidade"
        ],
        "categoria": "Assinaturas",
        "subcategoria": "Serviços Recorrentes"
    }
]

# ============================================================
# PIX (ANTES DE CARTÃO)
# ============================================================

REGRAS_PIX = [
    {
        "palavras": ["pix qrs autopass", "autopass"],
        "categoria": "Transporte",
        "subcategoria": "Mobilidade"
    },
    {
        "palavras": [
            "pix transf", "pix enviado", "pix recebido",
            "pix debito", "pix credito", "pix compra",
            "pix saque", "pix troco", "pix qr", "pix qrcode"
        ],
        "categoria": "Transferências",
        "subcategoria": "Pix"
    },
    {
        "palavras": ["qms interna", "confide22"],
        "categoria": "Transferências",
        "subcategoria": "Pix"
    }
]

# ============================================================
# PARCELAMENTO (BACKUP)
# ============================================================

REGRAS_PARCELAMENTO = [
    {
        "palavras": [
            "parcelado", "parcelamento", "parcela ",
            "parc ", "compra parc", "parc autorizada"
        ],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Parcelado"
    }
]

# ============================================================
# CARTÃO (BANDEIRAS E PRODUTOS)
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
    },
    {
        "palavras": ["c6 bank"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "C6 • Mastercard"
    },
    {
        "palavras": ["inter"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Inter • Mastercard"
    },
    {
        "palavras": ["bradesco prime"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "Bradesco • Visa"
    },
    {
        "palavras": ["xp visa"],
        "categoria": "Cartão de Crédito",
        "subcategoria": "XP • Visa Infinite"
    }
]

# ============================================================
# REGRAS GERAIS
# ============================================================

REGRAS_GERAIS = [

    # TRANSPORTE
    {
        "palavras": [
            "uber", "uber trip", "uber *", "99", "99pop", "99food",
            "cabify", "mobility", "mobilidade", "estapar", "zona azul",
            "estacionamento", "estac.", "shell box", "ipiranga",
            "posto", "combustivel", "gasolina"
        ],
        "categoria": "Transporte",
        "subcategoria": "Mobilidade"
    },

    # ALIMENTAÇÃO
    {
        "palavras": [
            "ifood", "ubereats", "rappi", "padaria", "restaurante",
            "lanchonete", "bar", "cafeteria", "café", "pizza",
            "burguer", "hamburguer", "sushi", "churrascaria",
            "bk", "burger king", "mcdonald", "habibs", "outback",
            "coco bambu", "madero", "giraffas"
        ],
        "categoria": "Alimentação",
        "subcategoria": "Refeições"
    },

    # SUPERMERCADO
    {
        "palavras": [
            "carrefour", "extra", "pao de acucar", "assai", "atacadao",
            "dia%", "mercado", "supermercado", "hortifruti",
            "sams club", "big", "natural da terra", "mundo verde"
        ],
        "categoria": "Alimentação",
        "subcategoria": "Supermercado"
    },

    # RENDA
    {
        "palavras": [
            "salario", "remuneracao", "provento", "pagamento",
            "holerite", "bonus", "comissao", "rendimento"
        ],
        "categoria": "Renda",
        "subcategoria": "Salário"
    },

    # SAÚDE
    {
        "palavras": [
            "droga", "drogasil", "droga raia", "farmacia", "remedio",
            "laboratorio", "exame", "clinica", "hospital",
            "paguemenos", "drogaria"
        ],
        "categoria": "Saúde",
        "subcategoria": "Gastos Médicos"
    },

    # LAZER
    {
        "palavras": [
            "cinema", "show", "evento", "teatro", "parque", "ingresso",
            "eventim", "sympla", "spotify festival"
        ],
        "categoria": "Lazer",
        "subcategoria": "Entretenimento"
    },

    # EDUCAÇÃO
    {
        "palavras": [
            "curso", "faculdade", "universidade", "escola",
            "alura", "udemy", "coursera", "senai", "senac",
            "fiap", "impacta", "estacio"
        ],
        "categoria": "Educação",
        "subcategoria": "Cursos"
    },

    # CASA
    {
        "palavras": [
            "casas bahia", "magalu", "magazine luiza", "lojas americanas",
            "tokstok", "tok&stok", "mobly", "etna", "construcao",
            "material", "ferramenta", "leroy merlin",
            "casatema", "madeira madeira"
        ],
        "categoria": "Casa",
        "subcategoria": "Manutenção"
    },

    # MORADIA
    {
        "palavras": [
            "aluguel", "condominio", "iptu", "luz", "energia",
            "enel", "copel", "sabesp", "sanepar", "agua",
            "cpfl", "cemig", "light"
        ],
        "categoria": "Moradia",
        "subcategoria": "Despesas Fixas"
    },

    # INTERNET / TELEFONIA
    {
        "palavras": [
            "vivo", "claro", "tim", "oi", "internet", "fibra",
            "telefone", "celular", "recarga",
            "claro box", "vivo fibra", "tim live"
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
            "submarino", "fastshop", "shein", "magalu",
            "casas bahia", "centauro"
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

    # 1. Assinaturas
    for regra in REGRAS_ASSINATURAS:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 2. PIX
    for regra in REGRAS_PIX:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 3. Parcelamento textual
    for regra in REGRAS_PARCELAMENTO:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 4. Cartão
    for regra in REGRAS_CARTAO:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 5. Gerais
    for regra in REGRAS_GERAIS:
        if any(p in desc for p in regra["palavras"]):
            return regra["categoria"], regra["subcategoria"]

    # 6. Fallback
    return "Outros", "A classificar"