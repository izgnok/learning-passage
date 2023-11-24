from dash import Dash, dcc, html, Output, Input, State, callback_context
from module.Firebase.firebase_manager import FirebaseManager
from flask_socketio import SocketIO
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import paramiko
import threading
import os
from dash.exceptions import PreventUpdate
from .layout import LayoutManager
from module.ElectricityMaps.electricity_maps import ElectricityMapsManager

class CallbackManager:
    """
    앱 콜백 스켈레톤 정의
    """
    def __init__(self, app, server):
        self.app = app # Dash에 대한 객체
        self.server = server # server에 대한 객체
        self.firebase = FirebaseManager() # Firebase에 대한 객체
        self.layout_manager = LayoutManager(self.app) #레이아웃 매니저 객체 생성
        self.pre_ev = 0 # ev 그래프 델타값 사용위해서
        self.cmp_ev = 0
        self.pre_emission = 0 # emission 그래프 델타값 사용위해서
        self.cmp_emission = 0
        self.pre_gfreq = 0 # gfreq 그래프 델타값 사용위해서
        self.cmp_gfreq = 0
        
    # RDB에서 컴퓨터 데이터를 읽어와서 정보를 반환하는 콜백함수
    def resources_callback(self):
        """
        컴퓨터 정보 콜백
        """
        @self.app.callback(
            Output('cpu','children'),
            Output('ram', 'children'),
            Output('gpu', 'children'),
            Input('interval-component', 'n_intervals'),
        )
        def update_resources_callback(n_intervals):
            # RDB에서 컴퓨터 정보 읽어오기
            cpu_name = self.firebase.read_data("com/CPU name")
            cpu_use = self.firebase.read_data("com/CPU useing")
            gpu_name = self.firebase.read_data("com/GPU name")
            gpu_use = self.firebase.read_data("com/GPU useing")
            ram_size = self.firebase.read_data("com/RAM size")
            ram_use = self.firebase.read_data("com/RAM useing")

            # 읽어온 정보로 직접 각 부분을 업데이트
            cpu_div = html.Div([
                html.Div("CPU", style={'font-size': '20px', 'font-weight': 'bold', 'margin-top': '8px'}),
                html.Div(f'CPU 아키텍처: {cpu_name}', style={'margin-top': '8px'}),
                html.Div(f'CPU 사용량: {cpu_use}', style={'margin-top': '8px'})
            ], id='cpu')
            ram_div = html.Div([
                html.Div("Memory", style={'font-size': '20px', 'font-weight': 'bold'}),
                html.Div(f'RAM 용량: {ram_size}', style={'margin-top': '8px'}),
                html.Div(f'RAM 사용량: {ram_use}', style={'margin-top': '8px'})
            ], id='ram')
            gpu_div = html.Div([
                html.Div("GPU", style={'font-size': '20px', 'font-weight': 'bold'}),
                html.Div(f'GPU 이름: {gpu_name}', style={'margin-top': '8px'}),
                html.Div(f'GPU 사용량: {gpu_use}', style={'margin-top': '8px'})
            ], id='gpu')
            # 업데이트된 정보를 tuple로 반환
            return cpu_div.children, ram_div.children, gpu_div.children


    # RDB에서 데이터를 읽어와서 그래프를 반환하는 콜백함수
    def graph_callback(self):
        """
        데이터, 그래프 콜백
        """
        @self.app.callback(
            Output('ev', 'figure'),
            Output('emission', 'figure'),
            Output('gfreq', 'figure'),
            Input('interval-component', 'n_intervals'),  # 주기적으로 콜백을 트리거합니다
        )
        def update_graph_callback(n_intervals):
            print("콜백이 트리거되었습니다!")

            #if not self.__user:
            #    raise PreventUpdate  # 사용자가 로그인하지 않았으면 업데이트하지 않음

            # Firebase에서 실시간 데이터 가져오기
            ev = self.firebase.read_data("main/ev")
            emission = self.firebase.read_data("main/emission")
            gfreq = self.firebase.read_data("main/gfreq")
            # 델타값 비교 알고리즘
            if(self.cmp_ev != ev): self.pre_ev = self.cmp_ev
            if(self.cmp_emission != emission): self.pre_emission = self.cmp_emission
            if(self.cmp_gfreq != gfreq): self.pre_gfreq = self.cmp_gfreq       
            self.cmp_ev = ev
            self.cmp_emission = emission
            self.cmp_gfreq = gfreq

            # 가져온 데이터를 레이아웃 데이터에 복사
            # 전력 사용량 그래프
            self.layout_manager.ev_use_fig = go.Figure(data = [go.Indicator(
                                                       mode="gauge+number+delta",
                                                       value=ev,
                                                       delta={'reference': self.pre_ev},
                                                       title={'text': "EV Usage(W)"},
                                                       domain={'x': [0,1], 'y': [0,1]},
                                                       gauge={'axis': {'range': [0,1000]}}
            )])
            #self.layout_manager.ev_use_fig = go.Figure(data=[go.Scatter(x=[1, 2, 3, 4], y=ev)]) # 다른그래프모양
            self.layout_manager.ev_use_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'서버 main: 전력 사용량')

            #탄소 배출량 그래프
            self.layout_manager.carbon_emission_fig = go.Figure(data=[go.Indicator(
                mode="gauge+number+delta",
                value=emission,
                gauge={
                    'shape':'bullet',
                    'axis':{'visible': True, 'range':[0,1000]},
                },
                delta={'reference': self.pre_emission},
                domain = {'x': [0.1, 1], 'y': [0.2, 0.9]},
            )])
            # 타이틀을 그래프 위로 올리기
            self.layout_manager.carbon_emission_fig.update_layout(annotations=[dict(
                text="Emission(g)",
                showarrow=False,
                xref="paper",
                yref="paper",
                x=0.5,
                y=0.98,
                align ="center",
                font=dict(
                        size=20, # 원하는 크기로 조절
                    ),
                )
            ])
            self.layout_manager.carbon_emission_fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), title=f'서버 main: 탄소 배출량')

            # GPU 주파수 그래프
            self.layout_manager.gpu_freq_fig = go.Figure(data=[go.Indicator(
                mode="gauge+number+delta",
                value=gfreq,
                delta={'reference': self.pre_gfreq},
                title={'text': "Frequency(Hz)"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={'axis': {'range': [0, 2000]}}
            )])
            self.layout_manager.gpu_freq_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'서버 main: GPU 주파수')

            # 그래프 반환
            return self.layout_manager.ev_use_fig, self.layout_manager.carbon_emission_fig, self.layout_manager.gpu_freq_fig


    def geo_callback():
        pass
