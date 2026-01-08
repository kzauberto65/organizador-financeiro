import plotly.express as px
import pandas as pd


# ============================================================
# GRÁFICOS EXISTENTES
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


def grafico_categoria(df_cat):
    df_cat = df_cat.sort_values("total_categoria", ascending=True)

    fig = px.bar(
        df_cat,
        x="total_categoria",
        y="categoria",
        orientation="h",
        title="Gastos por Categoria"
    )
    fig.update_layout(template="plotly_dark")
    return fig


def grafico_subcategoria(df_sub):
    df_sub = df_sub.sort_values("total_subcategoria", ascending=True)

    fig = px.bar(
        df_sub,
        x="total_subcategoria",
        y="subcategoria",
        orientation="h",
        title="Gastos por Subcategoria"
    )
    fig.update_layout(template="plotly_dark")
    return fig


def tabela_top10(df):
    df_sorted = df.sort_values("valor", ascending=False).head(10)
    return df_sorted


# ============================================================
# NOVOS GRÁFICOS INTELIGENTES
# ============================================================

def grafico_assinaturas(df):
    assinaturas = df[df["categoria"] == "Assinaturas"]

    if assinaturas.empty:
        fig = px.bar(title="Nenhuma assinatura encontrada")
        fig.update_layout(template="plotly_dark")
        return fig

    resumo = (
        assinaturas
        .groupby("descricao_normalizada")["valor"]
        .sum()
        .reset_index()
        .sort_values("valor", ascending=False)
    )

    fig = px.bar(
        resumo,
        x="descricao_normalizada",
        y="valor",
        title="Gastos com Assinaturas Recorrentes",
        text_auto=True
    )
    fig.update_layout(template="plotly_dark")
    return fig


def grafico_parcelamentos(df):
    parc = df[df["parcela_atual"].notna()].copy()   # <<< CORREÇÃO AQUI

    if parc.empty:
        fig = px.bar(title="Nenhum parcelamento encontrado")
        fig.update_layout(template="plotly_dark")
        return fig

    parc["label"] = parc.apply(
        lambda x: f"{x['descricao_normalizada']} ({int(x['parcela_atual'])}/{int(x['parcela_total'])})",
        axis=1
    )

    resumo = (
        parc.groupby("label")["valor"]
        .sum()
        .reset_index()
        .sort_values("valor", ascending=False)
    )

    fig = px.bar(
        resumo,
        x="label",
        y="valor",
        title="Parcelamentos Ativos",
        text_auto=True
    )
    fig.update_layout(template="plotly_dark")
    return fig


def grafico_transferencias_pf(df):
    transf = df[df["destinatario"].notna()].copy()  # <<< E AQUI TAMBÉM

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