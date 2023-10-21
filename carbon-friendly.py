from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

df = px.data.gapminder()
continents = df.continent.unique()
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

Logo = html.H1(
    "Carbon-friendly",
    className="bg-dark text-white p-2 mb-2 text-center"
)
loginForm = dbc.Form([
    dbc.Row([
        dbc.Col([
            dbc.Row(
                [
                    dbc.Label("ID", width="auto"),
                    dbc.Col(
                        dbc.Input(type="id", placeholder="아이디를 입력"),
                        className="me-3",
                    ),
                ],
                className="g-2",
            ),
            dbc.Row(
                [
                    dbc.Label("P W", width="auto"),
                    dbc.Col(
                        dbc.Input(type="password", placeholder="비밀번호 입력"),
                        className="me-3",
                    ),
                ],
                className="g-2",
            ),
        ], width=9),
        dbc.Col(dbc.Button("Submit", color="dark"), width="auto"),

    ]),
])

controls = dbc.Card(
    [Logo, loginForm],
    body=True,
)
resources = dbc.Card([html.H2("Computing Info🖥️"), 
                      html.Div("CPU"), 
                      html.Br(), 
                      html.Div("Memory"), 
                      html.Br(), 
                      html.Div("GPU")],
                     body=True)

top_graph = dcc.Graph(figure=fig)
geo = dcc.Graph(figure=fig)
app.layout = dbc.Container(
    [
        dbc.Row([
            dbc.Col([
                controls,
                dbc.Row(
                    resources
                )
            ], width=3),

            dbc.Col([
                dbc.Row([
                    dbc.Col(dbc.Card([html.Div(top_graph)], body=True, ), width=4),
                    dbc.Col(dbc.Card([html.Div(top_graph)], body=True, ), width=4),
                    dbc.Col(dbc.Card([html.Div(top_graph)], body=True, ), width=4),
                ]),
                dbc.Row([
                    dbc.Col(dbc.Card([html.Div(geo)], body=True))
                ]),
                dbc.Row([
                    dbc.Col(dbc.Card([html.Div(top_graph)], body=True, ), width=4),
                    dbc.Col(dbc.Card([html.Div(top_graph)], body=True, ), width=4),
                    dbc.Col(dbc.Card([html.Div(top_graph)], body=True, ), width=4),
                ]),
            ], width=9),
        ]),

    ],
    fluid=True,
    className="dbc dbc-ag-grid",
)

if __name__ == "__main__":
    app.run(debug=True)
    app.run_server()