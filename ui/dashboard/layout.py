from dash import dcc, html
import dash_bootstrap_components as dbc

def card(title, value, color):
    return dbc.Card(
        dbc.CardBody([
            html.H5(title, className="card-title"),
            html.H3(value, className="card-text")
        ]),
        style={"backgroundColor": color, "color": "white", "textAlign": "center"}
    )

def build_layout():
    return dbc.Container([

        # ============================
        # TÍTULO
        # ============================
        html.H1(
            "Dashboard Financeiro",
            style={
                "textAlign": "center",
                "color": "white",
                "marginTop": "20px",
                "marginBottom": "10px"
            }
        ),

        # ============================
        # CARDS
        # ============================
        dbc.Row([
            dbc.Col(id="card_saldo", width=4),
            dbc.Col(id="card_receitas", width=4),
            dbc.Col(id="card_despesas", width=4),
        ], style={"marginTop": "20px"}),

        # ============================
        # FILTROS
        # ============================
        dbc.Row([

            dbc.Col([
                html.Label("Mês", style={"color": "white"}),
                dcc.Dropdown(
                    id="filtro_mes",
                    placeholder="Selecione...",
                    className="dropdown-dark"
                )
            ], width=4),

            dbc.Col([
                html.Label("Categoria", style={"color": "white"}),
                dcc.Dropdown(
                    id="filtro_categoria",
                    placeholder="Selecione...",
                    className="dropdown-dark"
                )
            ], width=4),

            dbc.Col([
                html.Label("Tipo", style={"color": "white"}),
                dcc.Dropdown(
                    id="filtro_tipo",
                    options=[
                        {"label": "Receitas", "value": "receita"},
                        {"label": "Despesas", "value": "despesa"}
                    ],
                    placeholder="Selecione...",
                    className="dropdown-dark"
                )
            ], width=4),

        ], style={"marginTop": "20px"}),

        # ============================
        # BOTÃO LIMPAR
        # ============================
        dbc.Row([
            dbc.Col(
                dbc.Button(
                    "Limpar filtros",
                    id="btn_limpar",
                    color="secondary",
                    className="mt-2",
                    style={"width": "100%"}
                ),
                width=12
            )
        ], style={"marginTop": "10px"}),

        # ============================
        # TABS
        # ============================
        dcc.Tabs(
            id="tabs",
            value="tab_resumo",
            children=[
                dcc.Tab(label="Resumo", value="tab_resumo",
                        className="tab-dark", selected_className="tab-dark-selected"),

                dcc.Tab(label="Assinaturas", value="tab_assinaturas",
                        className="tab-dark", selected_className="tab-dark-selected"),

                dcc.Tab(label="Parcelamentos", value="tab_parcelamentos",
                        className="tab-dark", selected_className="tab-dark-selected"),

                dcc.Tab(label="Transferências PF", value="tab_transferencias",
                        className="tab-dark", selected_className="tab-dark-selected"),

                dcc.Tab(label="Top 10", value="tab_top10",
                        className="tab-dark", selected_className="tab-dark-selected"),

                dcc.Tab(label="Dados Brutos", value="tab_brutos",
                        className="tab-dark", selected_className="tab-dark-selected"),
            ],
            style={
                "marginTop": "20px",
                "borderRadius": "5px",
                "overflow": "hidden",
                "backgroundColor": "#222"
            }
        ),

        # ============================
        # ÁREA DE CONTEÚDO
        # ============================
        html.Div(
            id="conteudo",
            style={
                "marginTop": "20px",
                "color": "white",
                "paddingBottom": "40px"
            }
        )

    ],
    fluid=True,
    style={
        "backgroundColor": "#111",
        "minHeight": "100vh",
        "paddingBottom": "40px",
        "paddingLeft": "10px",
        "paddingRight": "10px"
    })