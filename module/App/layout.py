from dash import Dash, dcc, html
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

class LayoutManager:
    """
    앱 레이아웃 스켈레톤 정의
    """
    def __init__(self, app):
        self.app = app # Dash 인스턴스

        self.ev_use_fig = go.Figure(data = [go.Indicator(
                                                       mode="gauge+number",
                                                       title={'text': "EV Usage(W)"},
                                                       domain={'x': [0,1], 'y': [0,1]},
                                                       gauge={'axis': {'range': [0,1000]}}
        )])
        self.ev_use_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'# 서버: 전력 사용량')

        self.carbon_emission_fig = go.Figure(data=[go.Indicator( # 탄소배출량 그래프
                mode ="gauge+number",
                gauge={'shape':'bullet','axis':{'visible': False},},
                domain={'x': [0.1,1], 'y': [0.2,0.9]},
               
        )])
        # 타이틀을 그래프 위로 올리기
        self.carbon_emission_fig.update_layout(annotations=[dict(
                text="Emission(g)",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.98,
                align ="center",
                font=dict(
                    size=20, # 원하는 크기로 조절
                )
            )
        ])
        self.carbon_emission_fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), title=f'# 서버: 탄소 배출량')

        self.gpu_freq_fig = go.Figure(data=[go.Indicator(mode = "gauge+number",
                                                        title = {'text': "Frequency(Hz)"},
                                                        domain = {'x': [0, 1], 'y': [0, 1]},
                                                        gauge={'axis': {'range': [0, 2000]}})]) # GPU 사용량 그래프
        self.gpu_freq_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'# 서버: GPU 주파수')

        self.carbon_density_fig = go.Figure(data=[go.Indicator(mode= "gauge+number",
                                                               title={'text': 'Carbon-Intensity'},
                                                               domain ={'x':[0,1], 'y': [0,1]},
                                                               gauge={'axis': {'range': [0,1000]}}
                                                               )]) # 탄소 밀도 그래프
        self.carbon_density_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'탄소 밀집도: 지역#')

        self.energy_output_fig = go.Figure(data=go.Bar(
                y = ['원자력', '지열', '바이오매스','석탄','바람','태양','수력','양수','배터리용량','가스','오일','알수없음'],
                orientation='h'
        ))
        self.energy_output_fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), title=f'에너지 출처: 지역#')

        self.geo = go.Figure(data=go.Scattergeo(
            lon = [126.9780],
            lat = [37.5665],
            text = ['Seoul'],
            mode = 'markers',
            marker_color = 'rgb(255, 0, 0)',
            ))
        self.geo.update_layout(
            title = '물리적 서버 위치',
            geo_scope='asia',
            margin=dict(l=0, r=0, t=40, b=0)
        )   

        self.Logo = html.H1(
            "Carbon-friendly",
            className="bg-white text-black p-2 mb-2 text-center"
        )
        self.logo_path = "../../assets/img/logo.png" #로고 이미지 경로
        self.LogoImgForm = dbc.Container([
        dbc.Form([
                dbc.Row(
                    dbc.Col(html.Img(src=self.logo_path, height="300px"), width={"size": 10}),
                    className="d-flex justify-content-center align-items-center" #가운데정렬
                )]
            ),
        ],
        fluid=True,
        )

        self.controls = dbc.Card(
            [self.Logo, self.LogoImgForm],
            body=True,
        )

        self.resources = dbc.Container(
                        dbc.Card([html.H2("Computing Info 🖥️"), 
                                html.Div("CPU", id = 'cpu'), 
                                html.Br(), 
                                html.Div("GPU", id = 'gpu'), 
                                html.Br(), 
                                html.Div("Memory", id = 'ram')],
                                body=True)
        )
        
        # footer
        self.footer = html.Div([
                        html.P("© 2023 Data Science Lab All Rights Reserved."),
                        html.P([
                            html.P("49315. 부산광역시 사하구 낙동대로 550번길 37(하단동) 동아대학교 공과대학1호관 4층 423호"),
                            html.A("Lab Website", href="https://www.datasciencelabs.org/", target='_blank'),
                            html.A("Contact Us", href="https://github.com/datascience-labs", target='_blank'),
                            html.A("Maker github", href="https://github.com/jhparkland", target='_blank'),])
                        ],className="footer")


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
                            
                        ),
                        dcc.Interval(
                            id='interval-component',
                            interval=10000,  # 10초마다 콜백을 트리거하도록 설정
                            n_intervals=0
                        )
                    ], width=3),

                    dbc.Col([
                        dbc.Row([
                            dbc.Col(dbc.Card([html.Div(dcc.Graph(figure=self.carbon_emission_fig, id='emission'))], body=True, ), width=4),
                            dbc.Col(dbc.Card([html.Div(dcc.Graph(figure=self.ev_use_fig, id='ev'))], body=True, ), width=4),
                            dbc.Col(dbc.Card([html.Div(dcc.Graph(figure=self.gpu_freq_fig, id='gfreq'))], body=True, ), width=4),
                            dcc.Interval(
                                id='interval-component',
                                interval=10000,  # 10초마다 콜백을 트리거하도록 설정
                                n_intervals=0
                            )
                        ]),
                        dbc.Row([
                            dbc.Col(dbc.Card([html.Div(dcc.Graph(figure=self.geo))], body=True,))
                        ]),
                        dbc.Row([
                            dbc.Col(dbc.Card([html.Div(dcc.Graph(figure=self.carbon_density_fig, id='carbon_density'))], body=True, ), width=6),
                            dbc.Col(dbc.Card([html.Div(dcc.Graph(figure=self.energy_output_fig, id='energy_output'))], body=True, ), width=6),
                            dcc.Interval(
                                id='elec_interval-component',
                                interval=1000*60,  # 1분마다 콜백을 트리거하도록 설정
                                n_intervals=0
                            )
                        ]),
                    ], width=9),

                ]),
                self.footer,
            ],fluid=True, className="dbc dbc-ag-grid",)

