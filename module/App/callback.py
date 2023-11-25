from dash import Dash, dcc, html, Output, Input, State, callback_context
from module.Firebase.firebase import FirebaseManager
from flask_socketio import SocketIO
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import os
import random
from dash.exceptions import PreventUpdate
from .layout import LayoutManager
from module.ElectricityMaps.electricity_maps import ElectricityMapsManager
from datetime import datetime, timedelta

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
        self.em = ElectricityMapsManager() # Electiricty 매니저 객체 생성
        self.graph_count = 0 # 초기호출 확인 변수
        self.elec_count = 0 # 초기호출 확인 변수

    # RDB에서 컴퓨터 데이터를 읽어와서 정보를 반환하는 콜백함수
    def resources_callback(self):
        """
        컴퓨터 정보 콜백
        """
        @self.app.callback(
            [Output('cpu','children'),
            Output('ram', 'children'),
            Output('gpu', 'children')],
            Input('interval-component', 'n_intervals'),
        )
        def update_resources_callback(n_intervals):
            print("컴퓨터자원 콜백")
            # RDB에서 컴퓨터 정보 읽어오기
            cpu_name = self.firebase.read_data("com/CPU name")
            cpu_use = self.firebase.read_data("com/CPU useing")
            gpu_name = self.firebase.read_data("com/GPU name")
            gpu_use = self.firebase.read_data("com/GPU useing")
            ram_size = self.firebase.read_data("com/RAM size")
            ram_use = self.firebase.read_data("com/RAM useing")

            # 읽어온 정보로 직접 각 부분을 업데이트
            cpu_div = html.Div([
                dcc.Graph(
                            id='cpu_architecture',
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='gauge+number',  
                                        title=f"CPU ARCHITECTURE: {cpu_name}",  # Indicator 제목 설정
                                        value=float(cpu_use[:-1]),
                                        gauge = {'axis': {'range': [0, 100]}}

                            )
                        ],  'layout': {
                                'autosize': True,
                                'margin': {'l': 40, 'r': 40, 't': 0, 'b': 0},  # 여백 설정
                        } 
                            }
                        ),
            ], id='cpu')

            ram_div = html.Div([                
                dcc.Graph(
                            id='ram_size',
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='gauge+number',  
                                        title=f"RAM SIZE: {ram_size}",  # Indicator 제목 설정
                                        value=ram_use,
                                        gauge = {'axis': {'range': [0, 100]}}
                            )
                        ],  'layout': {
                                'autosize': True,
                                'margin': {'l': 40, 'r': 40, 't': 0, 'b': 0}  # 여백 설정
                        }    
                            }
                        ),
            ], id='ram')
            gpu_div = html.Div([
                # 그래프
                dcc.Graph(
                            id='gpu_name',
                            figure={
                                'data': [
                                    go.Indicator(
                                        mode='gauge+number',  
                                        title={'text': f"GPU NAME: {gpu_name}", 'font':{'size':16}},   # Indicator 제목 설정
                                        value=float(gpu_use),
                                        gauge = {'axis': {'range': [0, 100]}}

                            )
                        ],  'layout': {
                                'autosize': True,
                                'margin': {'l': 40, 'r': 40, 't': 0, 'b': 0}  # 여백 설정
                        }   
                            }
                        ),
            ], id='gpu')
            # 업데이트된 정보를 tuple로 반환
            return cpu_div.children, ram_div.children, gpu_div.children


    # RDB에서 데이터를 읽어와서 그래프를 반환하는 콜백함수
    def graph_callback(self):
        """
        데이터, 그래프 콜백
        """
        @self.app.callback(
            [Output('ev', 'figure'),
            Output('emission', 'figure'),
            Output('gfreq', 'figure')],
            [Input('interval-component', 'n_intervals'),  # 주기적으로 콜백을 트리거합니다
            Input('zone', 'children')],
            allow_duplicate=True
        )
        def update_graph_callback(n_intervals, children):
            ctx = callback_context
            print(self.graph_count)
            if ctx.triggered_id == 'zone' and self.graph_count != 0:
                if children is None:
                    return self.layout_manager.ev_use_fig, self.layout_manager.carbon_emission_fig, self.layout_manager.gpu_freq_fig   
            
            self.graph_count = 1 #초기호출 완료
            print('그래프 콜백')
            #현재 서버나라 읽어오기
            zone = self.firebase.read_data("main/zone")
            #랜덤데이터 RDB에 넣기        
            random_emission = random.randint(50,330)
            random_ev = random.randint(300,450)
            random_gfreq = random.randint(750,2000)
            self.firebase.write_data(f"{zone}/emission",random_emission)
            self.firebase.write_data(f"{zone}/ev",random_ev)
            self.firebase.write_data(f"{zone}/gfreq",random_gfreq)

            # Firebase에서 실시간 데이터 가져오기
            ev = self.firebase.read_data(f"{zone}/ev")
            cmp_ev = self.firebase.read_data(f"{zone}/cmpev")
            pre_ev = self.firebase.read_data(f"{zone}/preev")
            emission = self.firebase.read_data(f"{zone}/emission")
            cmp_emission = self.firebase.read_data(f"{zone}/cmpemission")
            pre_emission = self.firebase.read_data(f"{zone}/preemission")
            gfreq = self.firebase.read_data(f"{zone}/gfreq")
            cmp_gfreq = self.firebase.read_data(f"{zone}/cmpgfreq")
            pre_gfreq = self.firebase.read_data(f"{zone}/pregfreq")
            if(zone=='KR'): country ="대한민국"
            if(zone=='JP-TK'): country ="일본"
            if(zone=='DE'): country ="독일"
            if(zone=='FR'): country ="프랑스"
            # 델타값 비교 알고리즘
            if(cmp_ev != ev): 
                pre_ev = cmp_ev
                self.firebase.write_data(f"{zone}/preev", pre_ev)
            if(cmp_emission != emission):
                pre_emission = cmp_emission
                self.firebase.write_data(f"{zone}/preemission", pre_emission)
            if(cmp_gfreq != gfreq):
                pre_gfreq = cmp_gfreq 
                self.firebase.write_data(f"{zone}/pregfreq", pre_gfreq)
            self.firebase.write_data(f"{zone}/cmpev", ev)
            self.firebase.write_data(f"{zone}/cmpemission", emission)
            self.firebase.write_data(f"{zone}/cmpgfreq", gfreq)


            # 가져온 데이터를 레이아웃 데이터에 복사
            # 전력 사용량 그래프
            self.layout_manager.ev_use_fig = go.Figure(data = [go.Indicator(
                                                       mode="gauge+number+delta",
                                                       value=ev,
                                                       delta={'reference': pre_ev},
                                                       title={'text': "EV Usage(W)"},
                                                       domain={'x': [0,1], 'y': [0,1]},
                                                       gauge={'axis': {'range': [0,1000]}}
            )])
            #self.layout_manager.ev_use_fig = go.Figure(data=[go.Scatter(x=[1, 2, 3, 4], y=ev)]) # 다른그래프모양
            self.layout_manager.ev_use_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'{country} 서버: 전력 사용량')

            #탄소 배출량 그래프
            self.layout_manager.carbon_emission_fig = go.Figure(data=[go.Indicator(
                mode="gauge+number+delta",
                value=emission,
                gauge={
                    'shape':'bullet',
                    'axis':{'visible': True, 'range':[0,500]},
                },
                delta={'reference': pre_emission},
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
            self.layout_manager.carbon_emission_fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), title=f'{country} 서버: 탄소 배출량')

            # GPU 주파수 그래프
            self.layout_manager.gpu_freq_fig = go.Figure(data=[go.Indicator(
                mode="gauge+number+delta",
                value=gfreq,
                delta={'reference': pre_gfreq},
                title={'text': "Frequency(Hz)"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={'axis': {'range': [0, 2000]}}
            )])
            self.layout_manager.gpu_freq_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'{country} 서버: GPU 주파수')

            # 그래프 반환
            return self.layout_manager.ev_use_fig, self.layout_manager.carbon_emission_fig, self.layout_manager.gpu_freq_fig

    #일렉트리시티API 콜백
    def electricity_callback(self):
        @self.app.callback(
            [Output('carbon_density', 'figure'),
            Output('energy_output', 'figure')],
            [Input('elec_interval-component', 'n_intervals'),  # 주기적으로 콜백을 트리거합니다
            Input('zone', 'children')],
            allow_duplicate=True
        )
        def update_electricity_callback(n_intervals,children):
            ctx = callback_context
            if ctx.triggered_id == 'zone' and self.elec_count!=0:
                if children is None:
                    return self.layout_manager.carbon_density_fig, self.layout_manager.energy_output_fig 
            
            self.elec_count = 1 #초기호출완료
            print('elec 콜백')
            # 데이터 랜덤 삽입
            # random_country = random.choice(["KR", "JP-TK", "DE", "FR"])
            # self.firebase.write_data("main/zone",random_country)

            # 데이터 읽어오기
            zone = self.firebase.read_data("main/zone")
            carbon_data = self.em.carbon_intensity("carbon-intensity",zone = zone, format='latest')
            # 특정국가 평균 탄소 밀집도 < 현재 탄소 밀집도 조건 확인 Flag 전송
            if(zone == 'KR'):
                if(carbon_data.get('carbonIntensity') > 435):
                    self.firebase.write_data("optim/request", True)
                else: self.firebase.write_data("optim/request", False)
            if(zone == 'DE'):
                if(carbon_data.get('carbonIntensity') > 420):
                    self.firebase.write_data("optim/request", True)
                else: self.firebase.write_data("optim/request", False)
            if(zone == 'JP-TK'):
                if(carbon_data.get('carbonIntensity') > 480):
                    self.firebase.write_data("optim/request", True)
                else: self.firebase.write_data("optim/request", False)
            if(zone == 'FR'):
                if(carbon_data.get('carbonIntensity') > 50):
                    self.firebase.write_data("optim/request", True)
                else: self.firebase.write_data("optim/request", False)

            power_data_all = self.em.carbon_intensity("power-breakdown",zone = zone, format='latest')
            power_data = power_data_all.get("powerProductionBreakdown")
            if(zone=='KR'): country ="대한민국"
            if(zone=='JP-TK'): country ="일본"
            if(zone=='DE'): country ="독일"
            if(zone=='FR'): country ="프랑스"
            nuclear = power_data.get("nuclear") # 원자력
            geothermal = power_data.get("geothermal") # 지열
            biomass = power_data.get("biomass") # 바이오매스
            coal = power_data.get("coal") # 석탄
            wind = power_data.get("wind") # 바람
            solar = power_data.get("solar") # 태양
            hydro = power_data.get("hydro") # 수력
            hydro_discharge = power_data.get("hydro discharge") # 양수
            battery_discharge = power_data.get("battery discharge") # 배터리 용량
            gas = power_data.get("gas") # 가스
            oil = power_data.get("oil") # 오일
            unknown = power_data.get("unknown") # 알수없음
            # 시간읽어와서 형식바꾸기 ( +9시 )
            carbon_datetime = datetime.strptime(carbon_data.get("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=9)
            power_datetime = datetime.strptime(power_data_all.get("datetime"), "%Y-%m-%dT%H:%M:%S.%fZ") + timedelta(hours=9)
            carbon_date = carbon_datetime.strftime("%Y-%m-%d")
            carbon_time = carbon_datetime.strftime("%H시")
            power_date = power_datetime.strftime("%Y-%m-%d")
            power_time = power_datetime.strftime("%H시")
            # 델타값 비교 알고리즘
            cmp_intensity = self.firebase.read_data(f"{zone}/cmpintensity")
            pre_intensity = self.firebase.read_data(f"{zone}/preintensity")
            if(cmp_intensity != carbon_data.get('carbonIntensity')): 
                pre_intensity = carbon_data.get('carbonIntensity')
                self.firebase.write_data(f"{zone}/preintensity", pre_intensity)
                self.firebase.write_data(f"{zone}/cmpintensity", carbon_data.get('carbonIntensity'))
            

            #탄소밀집도 그래프
            self.layout_manager.carbon_density_fig = go.Figure(data=[go.Indicator(mode= "gauge+number+delta",
                                                               title={'text': 'Carbon-Intensity'},
                                                               value=carbon_data.get('carbonIntensity'),
                                                               domain ={'x':[0,1], 'y': [0,1]},
                                                               gauge={'axis': {'range': [0,1000]}},
                                                               delta={'reference': pre_intensity},
                                                               )]) 
            self.layout_manager.carbon_density_fig.update_layout(margin=dict(l=40, r=40, t=40, b=0), title=f'탄소밀집도: {country} ({carbon_date} {carbon_time})')

            # 에너지 출처 그래프
            self.layout_manager.energy_output_fig = go.Figure(data=go.Bar(
                x = [nuclear, geothermal, biomass, coal, wind, solar, hydro, hydro_discharge, battery_discharge, gas, oil, unknown],
                y = ['원자력', '지열', '바이오매스','석탄','바람','태양','수력','댐','배터리용량','가스','오일','알수없음'],
                orientation='h'
            ))
            self.layout_manager.energy_output_fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), title=f'에너지 출처: {country} ({power_date} {power_time})')

            return self.layout_manager.carbon_density_fig, self.layout_manager.energy_output_fig

    def electricity_callback2(self):
        @self.app.callback(
            Output('zone', 'children'),
            Input('elec_interval-component2', 'n_intervals')
        )
        def update_electricity_callback2(n_intervals):
            print('플래그체크 콜백')
            zone = None
            if self.firebase.read_data('optim/changed'): 
                zone = self.firebase.read_data("main/zone")
                self.firebase.write_data('optim/changed', False)
                print(f'{zone}으로 바뀜')
            return zone

    def geo_callback(self):
        @self.app.callback(
            Output('url', 'children'),
            Input('map', 'clickData'),  # 주기적으로 콜백을 트리거합니다
        )
        def update_url(clickData):
            pass
            