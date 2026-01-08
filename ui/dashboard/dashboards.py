import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from dash import dash_table
from pathlib import Path
import pandas as pd
import webbrowser
import os

from charts import (
    grafico_evolucao,
    grafico_categoria,
    grafico_subcategoria,
    grafico_assinaturas,
    grafico_parcelamentos,
    grafico_transferencias_pf
)

from layout import build_layout

# Caminho correto para a pasta financas/
BASE_DIR = Path(__file__).resolve().parents[2]


# ============================
# CARREGAMENTO DE DADOS
# ============================

def carregar_dados():
    mensal = pd.read_parquet(BASE_DIR / "analises/mensal.parquet")
    categoria = pd.read_parquet(BASE_DIR / "analises/categoria.parquet")
    subcategoria = pd.read_parquet(BASE_DIR / "analises/subcategoria.parquet")
    normalizado = pd.read_parquet(BASE_DIR / "normalizado/itau/conta_corrente.parquet")
    return mensal, categoria, subcategoria, normalizado


# ============================
# FORMATADORES
# ============================

def formatar_top10(df):
    df = df.copy()

    df["valor"] = df["valor"].apply(
        lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )

    df["data_lancamento"] = pd.to_datetime(df["data_lancamento"], errors="coerce") \
        .dt.strftime("%d/%m/%Y")

    df = df.fillna("")
    return df


# ============================
# INICIAR DASHBOARD
# ============================

def iniciar_dashboard():
    mensal, categoria, subcategoria, normalizado = carregar_dados()

    config_plot = {
        "displaylogo": False,
        "showSendToCloud": False,
        "modeBarButtonsToRemove": ["sendDataToCloud"]
    }

    top10_df = formatar_top10(normalizado.nlargest(10, "valor"))

    charts = {
        "evolucao_mensal": dcc.Graph(
            figure=grafico_evolucao(mensal),
            config=config_plot
        ),
        "categoria": dcc.Graph(
            figure=grafico_categoria(categoria),
            config=config_plot
        ),
        "subcategoria": dcc.Graph(
            figure=grafico_subcategoria(subcategoria),
            config=config_plot
        ),

        "top10": dash_table.DataTable(
            data=top10_df.to_dict("records"),
            columns=[{"name": col, "id": col} for col in top10_df.columns],
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
        ),

        "assinaturas": dcc.Graph(
            figure=grafico_assinaturas(normalizado),
            config=config_plot
        ),
        "parcelamentos": dcc.Graph(
            figure=grafico_parcelamentos(normalizado),
            config=config_plot
        ),
        "transferencias_pf": dcc.Graph(
            figure=grafico_transferencias_pf(normalizado),
            config=config_plot
        ),

        "dados_brutos": html.Pre(normalizado.head(50).to_string())
    }

    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])
    app.layout = build_layout(charts)

    @app.callback(
        Output("conteudo", "children"),
        Input("tabs", "value")
    )
    def render_tab(tab):
        if tab == "tab_resumo":
            return html.Div([
                charts["evolucao_mensal"],
                charts["categoria"],
                charts["subcategoria"]
            ])

        elif tab == "tab_assinaturas":
            return charts["assinaturas"]

        elif tab == "tab_parcelamentos":
            return charts["parcelamentos"]

        elif tab == "tab_transferencias":
            return charts["transferencias_pf"]

        elif tab == "tab_top10":
            return html.Div([
                html.H3("Top 10 Despesas"),
                charts["top10"]
            ])

        elif tab == "tab_brutos":
            return html.Div([
                html.H3("Dados Brutos (primeiras 50 linhas)"),
                charts["dados_brutos"]
            ])

    app.run(debug=True)


# ============================
# EXECUÇÃO DIRETA
# ============================

if __name__ == "__main__":
    # Abre o navegador apenas uma vez, evitando duplicação
    if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
        webbrowser.open("http://127.0.0.1:8050/")

    iniciar_dashboard()