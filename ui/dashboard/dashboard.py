import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dash_table
from dash import callback_context
import pandas as pd
from pathlib import Path
import os
import webbrowser

from charts import (
    grafico_evolucao,
    grafico_categoria,
    grafico_subcategoria,
    grafico_assinaturas,
    grafico_parcelamentos,
    grafico_transferencias_pf
)

from layout import build_layout, card

# Detecta raiz do projeto
def get_project_root():
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / "rodar.py").exists():
            return parent
    return current.parents[1]

BASE_DIR = get_project_root()

# Carrega dados
def carregar_dados():
    mensal = pd.read_parquet(BASE_DIR / "analises/mensal.parquet")
    categoria = pd.read_parquet(BASE_DIR / "analises/categoria.parquet")
    subcategoria = pd.read_parquet(BASE_DIR / "analises/subcategoria.parquet")
    normalizado = pd.read_parquet(BASE_DIR / "normalizado/itau/transacoes.parquet")
    normalizado["data_lancamento"] = pd.to_datetime(normalizado["data_lancamento"], errors="coerce")
    return mensal, categoria, subcategoria, normalizado

def iniciar_dashboard():
    mensal_raw, categoria_raw, subcategoria_raw, normalizado = carregar_dados()

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    app.layout = build_layout()

    # Cards de resumo (sempre com base no DF filtrado)
    @app.callback(
        Output("card_saldo", "children"),
        Output("card_receitas", "children"),
        Output("card_despesas", "children"),
        Input("filtro_mes", "value"),
        Input("filtro_categoria", "value"),
        Input("filtro_tipo", "value"),
        Input("btn_limpar", "n_clicks")
    )
    def atualizar_cards(mes, categoria_filtro, tipo, limpar):
        df = normalizado.copy()

        if mes:
            df = df[df["data_lancamento"].dt.to_period("M").astype(str) == mes]

        if categoria_filtro:
            df = df[df["categoria"] == categoria_filtro]

        if tipo == "receita":
            df = df[df["valor"] > 0]
        elif tipo == "despesa":
            df = df[df["valor"] < 0]

        total_receitas = df[df["valor"] > 0]["valor"].sum()
        total_despesas = df[df["valor"] < 0]["valor"].sum()
        saldo = total_receitas + total_despesas

        return (
            card("Saldo", f"R$ {saldo:,.2f}", "#444"),
            card("Receitas", f"R$ {total_receitas:,.2f}", "green"),
            card("Despesas", f"R$ {total_despesas:,.2f}", "red"),
        )

    # Preenche filtros de mês e categoria
    @app.callback(
        Output("filtro_mes", "options"),
        Output("filtro_categoria", "options"),
        Input("tabs", "value")
    )
    def preencher_filtros(_):
        meses = normalizado["data_lancamento"].dropna().dt.to_period("M").astype(str).unique()
        categorias = normalizado["categoria"].dropna().unique()

        opcoes_mes = [{"label": m, "value": m} for m in sorted(meses)]
        opcoes_cat = [{"label": c, "value": c} for c in sorted(categorias)]

        return opcoes_mes, opcoes_cat

    # ÚNICO callback que controla conteúdo + filtros + limpar
    @app.callback(
        Output("conteudo", "children"),
        Output("filtro_mes", "value"),
        Output("filtro_categoria", "value"),
        Output("filtro_tipo", "value"),
        Input("tabs", "value"),
        Input("filtro_mes", "value"),
        Input("filtro_categoria", "value"),
        Input("filtro_tipo", "value"),
        Input("btn_limpar", "n_clicks")
    )
    def atualizar_conteudo(tab, mes, categoria_filtro, tipo, limpar):

        triggered = callback_context.triggered[0]["prop_id"] if callback_context.triggered else ""

        if "btn_limpar" in triggered:
            mes = None
            categoria_filtro = None
            tipo = None

        # ============================
        # FILTRAGEM DO DF BASE
        # ============================
        df = normalizado.copy()

        if mes:
            df = df[df["data_lancamento"].dt.to_period("M").astype(str) == mes]

        if categoria_filtro:
            df = df[df["categoria"] == categoria_filtro]

        if tipo == "receita":
            df = df[df["valor"] > 0]
        elif tipo == "despesa":
            df = df[df["valor"] < 0]

        # ============================
        # REAGREGAÇÃO PARA A ABA RESUMO
        # ============================

        # Evolução mensal filtrada
        mensal = df.copy()
        mensal["ano_mes"] = mensal["data_lancamento"].dt.to_period("M").astype(str)
        mensal = mensal.groupby("ano_mes")["valor"].sum().reset_index()
        mensal.rename(columns={"valor": "total_mes"}, inplace=True)

        # Categoria filtrada
        categoria = df.groupby("categoria")["valor"].sum().reset_index()
        categoria.rename(columns={"valor": "total_categoria"}, inplace=True)

        # Subcategoria filtrada
        subcategoria = df.groupby("subcategoria")["valor"].sum().reset_index()
        subcategoria.rename(columns={"valor": "total_subcategoria"}, inplace=True)

        # ============================
        # RENDERIZAÇÃO DAS ABAS
        # ============================

        if tab == "tab_resumo":
            fig_cat_r, fig_cat_d = grafico_categoria(categoria)
            fig_sub_r, fig_sub_d = grafico_subcategoria(subcategoria)

            conteudo = html.Div([
                dcc.Graph(figure=grafico_evolucao(mensal)),

                dbc.Row([
                    dbc.Col(dcc.Graph(figure=fig_cat_r), width=6),
                    dbc.Col(dcc.Graph(figure=fig_cat_d), width=6),
                ]),

                dbc.Row([
                    dbc.Col(dcc.Graph(figure=fig_sub_r), width=6),
                    dbc.Col(dcc.Graph(figure=fig_sub_d), width=6),
                ]),
            ])

            return conteudo, mes, categoria_filtro, tipo

        elif tab == "tab_assinaturas":
            return dcc.Graph(figure=grafico_assinaturas(df)), mes, categoria_filtro, tipo

        elif tab == "tab_parcelamentos":
            return dcc.Graph(figure=grafico_parcelamentos(df)), mes, categoria_filtro, tipo

        elif tab == "tab_transferencias":
            return dcc.Graph(figure=grafico_transferencias_pf(df)), mes, categoria_filtro, tipo

        elif tab == "tab_top10":
            top10 = df.nlargest(10, "valor").copy()
            if not top10.empty:
                top10["valor"] = top10["valor"].apply(
                    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
                )
                top10["data_lancamento"] = top10["data_lancamento"].dt.strftime("%d/%m/%Y")
                top10 = top10.fillna("")

            tabela = dash_table.DataTable(
                data=top10.to_dict("records"),
                columns=[{"name": col, "id": col} for col in top10.columns],
                style_table={"overflowX": "auto"},
                style_cell={
                    "padding": "8px",
                    "border": "1px solid #444",
                    "backgroundColor": "#222",
                    "color": "white",
                    "fontFamily": "Arial",
                    "fontSize": "14px",
                },
                style_header={
                    "backgroundColor": "#111",
                    "fontWeight": "bold",
                    "border": "1px solid #555",
                },
                style_data_conditional=[
                    {"if": {"row_index": "odd"}, "backgroundColor": "#2b2b2b"}
                ],
            )

            conteudo = html.Div(
                [html.H4("Top 10 Despesas", style={"marginBottom": "20px"}), tabela],
                style={"backgroundColor": "#111", "padding": "10px"}
            )
            return conteudo, mes, categoria_filtro, tipo

        elif tab == "tab_brutos":
            texto = df.head(50).to_string()
            conteudo = html.Div([
                html.H4("Dados Brutos", style={"color": "white", "marginBottom": "10px"}),
                html.Pre(texto, style={"color": "white", "backgroundColor": "#111", "padding": "10px"})
            ])
            return conteudo, mes, categoria_filtro, tipo

        return html.Div("Aba não encontrada."), mes, categoria_filtro, tipo

    app.run(debug=True)

if __name__ == "__main__":
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://127.0.0.1:8050/")
    iniciar_dashboard()