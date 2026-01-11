import plotly.express as px
import pandas as pd

# ============================================================
# EVOLUÇÃO MENSAL
# ============================================================

def grafico_evolucao(df_mensal):
    fig = px.line(
        df_mensal,
        x="ano_mes",
        y="total_mes",
        title="Evolução Mensal",
        markers=True
    )
    fig.update_layout(template="plotly_dark")
    return fig


# ============================================================
# CATEGORIAS — RECEITAS E DESPESAS SEPARADAS
# ============================================================

def grafico_categoria(df_cat):
    df = df_cat.copy()

    df["categoria"] = df["categoria"].replace({
        "Transferência": "Transferências",
        "transferência": "Transferências"
    })

    receitas = df[df["total_categoria"] > 0].sort_values("total_categoria")
    despesas = df[df["total_categoria"] < 0].sort_values("total_categoria")

    fig_receita = px.bar(
        receitas,
        x="total_categoria",
        y="categoria",
        orientation="h",
        title="Receitas por Categoria",
        color_discrete_sequence=["green"]
    )
    fig_receita.update_layout(template="plotly_dark")

    fig_despesa = px.bar(
        despesas,
        x="total_categoria",
        y="categoria",
        orientation="h",
        title="Despesas por Categoria",
        color_discrete_sequence=["red"]
    )
    fig_despesa.update_layout(template="plotly_dark")

    return fig_receita, fig_despesa


# ============================================================
# SUBCATEGORIAS — RECEITAS E DESPESAS SEPARADAS
# ============================================================

def grafico_subcategoria(df_sub):
    df = df_sub.copy()

    receitas = df[df["total_subcategoria"] > 0].sort_values("total_subcategoria")
    despesas = df[df["total_subcategoria"] < 0].sort_values("total_subcategoria")

    fig_receita = px.bar(
        receitas,
        x="total_subcategoria",
        y="subcategoria",
        orientation="h",
        title="Receitas por Subcategoria",
        color_discrete_sequence=["green"]
    )
    fig_receita.update_layout(template="plotly_dark")

    fig_despesa = px.bar(
        despesas,
        x="total_subcategoria",
        y="subcategoria",
        orientation="h",
        title="Despesas por Subcategoria",
        color_discrete_sequence=["red"]
    )
    fig_despesa.update_layout(template="plotly_dark")

    return fig_receita, fig_despesa


# ============================================================
# ASSINATURAS
# ============================================================

def grafico_assinaturas(df):
    assinaturas = df[df["categoria"] == "Assinaturas"]

    if assinaturas.empty:
        fig = px.bar(title="Nenhuma assinatura encontrada")
        fig.update_layout(template="plotly_dark")
        return fig

    resumo = (
        assinaturas.groupby("descricao_normalizada")["valor"]
        .sum()
        .reset_index()
        .sort_values("valor", ascending=False)
    )

    fig = px.bar(
        resumo,
        x="descricao_normalizada",
        y="valor",
        title="Gastos com Assinaturas",
        text_auto=True
    )
    fig.update_layout(template="plotly_dark")
    return fig


# ============================================================
# PARCELAMENTOS
# ============================================================

def grafico_parcelamentos(df):
    df = df.copy()

    if "parcela_atual" not in df.columns:
        df["parcela_atual"] = None

    parc = df[df["parcela_atual"].notna()].copy()

    if parc.empty:
        fig = px.bar(title="Nenhum parcelamento encontrado")
        fig.update_layout(template="plotly_dark")
        return fig

    parc["label"] = parc.apply(
        lambda x: f"{x['descricao_normalizada']} ({int(x['parcela_atual'])}/{int(x['parcela_total'])})",
        axis=1
    )

    fig = px.bar(
        parc,
        x="label",
        y="valor",
        title="Parcelamentos",
        text="valor"
    )
    fig.update_layout(template="plotly_dark")
    return fig


# ============================================================
# TRANSFERÊNCIAS PF
# ============================================================

def grafico_transferencias_pf(df):
    df = df.copy()

    if "destinatario" not in df.columns:
        df["destinatario"] = None

    transf = df[df["destinatario"].notna()].copy()

    if transf.empty:
        fig = px.bar(title="Nenhuma transferência para PF encontrada")
        fig.update_layout(template="plotly_dark")
        return fig

    resumo = (
        transf.groupby("destinatario")["valor"]
        .sum()
        .reset_index()
        .sort_values("valor", ascending=False)
    )

    fig = px.bar(
        resumo,
        x="destinatario",
        y="valor",
        title="Transferências para Pessoas Físicas",
        text_auto=True
    )
    fig.update_layout(template="plotly_dark")
    return fig