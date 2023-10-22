from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

class LayoutManager:
    """
    앱 레이아웃 스켈레톤 정의
    """

    def __init__(self, app):
        self.app = app
        fig = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[4, 1, 2])])
        fig.update_layout(margin=dict(l=0, r=0, t=0, b=0))

        self.Logo = html.H1(
            "Carbon-friendly",
            className="bg-dark text-white p-2 mb-2 text-center"
        )
        self.loginForm = dbc.Form([
            dbc.Row([
                dbc.Col([
                    dbc.Row(
                        [
                            dbc.Label("ID", width="auto"),
                            dbc.Col(
                                dbc.Input(type="id", placeholder="아이디를 입력", id = 'id'),
                                className="me-3",
                            ),
                        ],
                        className="g-2",
                    ),
                    dbc.Row(
                        [
                            dbc.Label("P W", width="auto"),
                            dbc.Col(
                                dbc.Input(type="password", placeholder="비밀번호 입력", id = 'pw'),
                                className="me-3",
                            ),
                        ],
                        className="g-2",
                    ),
                ], width=9),
                dbc.Col(dbc.Button("Submit", color="dark", id = 'loginbtn'), width="auto"),

            ]),
        ])

        self.controls = dbc.Card(
            [self.Logo, self.loginForm],
            body=True,
        )

        self.resources = dbc.Container(
                        dbc.Card([html.H2("Computing Info🖥️"), 
                                html.Div("CPU", id = 'cpu'), 
                                html.Br(), 
                                html.Div("Memory", id = 'ram'), 
                                html.Br(), 
                                html.Div("GPU", id = 'gpu')],
                                body=True)
                    )
        
        # 나중에 figure 인자 지워야 함. 추후 콜백으로 그래프를 리턴함.
        self.top_graph = dcc.Graph(figure=fig, id = 'top_graph')
        self.bottom_graph = dcc.Graph(figure=fig, id = 'bottom_graph')
        self.geo = dcc.Graph(figure=fig, id = 'geo')

    def create_layout(self):
        """
        앱 레이아웃 생성

        Returns:
            _type_: 사전에 정의된 레이아웃 요소로 부터 레이아웃 생성
        """
        return dbc.Container([
                dbc.Row([
                    dbc.Col([
                        self.controls,
                        dbc.Row(
                            self.resources
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Row([
                            dbc.Col(dbc.Card([html.Div(self.top_graph)], body=True, ), width=4),
                            dbc.Col(dbc.Card([html.Div(self.top_graph)], body=True, ), width=4),
                            dbc.Col(dbc.Card([html.Div(self.top_graph)], body=True, ), width=4),
                        ]),
                        dbc.Row([
                            dbc.Col(dbc.Card([html.Div(self.geo)], body=True))
                        ]),
                        dbc.Row([
                            dbc.Col(dbc.Card([html.Div(self.bottom_graph)], body=True, ), width=4),
                            dbc.Col(dbc.Card([html.Div(self.bottom_graph)], body=True, ), width=4),
                            dbc.Col(dbc.Card([html.Div(self.bottom_graph)], body=True, ), width=4),
                        ]),
                    ], width=9),
                ]),
                #footer
                html.Div(
                        [
                            html.P("© 2023 Data Science Lab All Rights Reserved."),
                            html.P([
                                    html.P("49315. 부산광역시 사하구 낙동대로 550번길 37(하단동) 동아대학교 공과대학1호관 4층 423호"),
                                    html.A("Lab Website", href="https://www.datasciencelabs.org/", target='_blank'),
                                    html.A("Contact Us", href="https://github.com/datascience-labs", target='_blank'),
                                    html.A("Maker github", href="https://github.com/jhparkland", target='_blank'),])
                        ],className="footer"),
            ],fluid=True, className="dbc dbc-ag-grid",)

