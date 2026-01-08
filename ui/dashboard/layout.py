from dash import dcc, html
import dash_bootstrap_components as dbc


def build_layout(charts):
    return dbc.Container([
        html.H1(
            "Dashboard Financeiro",
            style={"textAlign": "center", "marginTop": "20px"}
        ),

        dcc.Tabs(
            id="tabs",
            value="tab_resumo",
            children=[
                dcc.Tab(label="Resumo", value="tab_resumo",
                        style={"color": "white", "backgroundColor": "#222"},
                        selected_style={"color": "white", "backgroundColor": "#444"}),

                dcc.Tab(label="Assinaturas", value="tab_assinaturas",
                        style={"color": "white", "backgroundColor": "#222"},
                        selected_style={"color": "white", "backgroundColor": "#444"}),

                dcc.Tab(label="Parcelamentos", value="tab_parcelamentos",
                        style={"color": "white", "backgroundColor": "#222"},
                        selected_style={"color": "white", "backgroundColor": "#444"}),

                dcc.Tab(label="Transferências PF", value="tab_transferencias",
                        style={"color": "white", "backgroundColor": "#222"},
                        selected_style={"color": "white", "backgroundColor": "#444"}),

                dcc.Tab(label="Top 10", value="tab_top10",
                        style={"color": "white", "backgroundColor": "#222"},
                        selected_style={"color": "white", "backgroundColor": "#444"}),

                dcc.Tab(label="Dados Brutos", value="tab_brutos",
                        style={"color": "white", "backgroundColor": "#222"},
                        selected_style={"color": "white", "backgroundColor": "#444"}),
            ],
            style={"marginTop": "20px"}
        ),

        html.Div(id="conteudo", style={"marginTop": "20px"})
    ], fluid=True)