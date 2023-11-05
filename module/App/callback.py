from dash import Dash, dcc, html, Output, Input, State, callback_context
from module.Firebase.firebase import FirebaseManager
from flask_socketio import SocketIO
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go
import paramiko
import threading
import os

class CallbackManager:
    """
    앱 콜백 스켈레톤 정의
    """

    def __init__(self, app, server):
        self.app = app # Dash에 대한 객체
        self.server = server # server에 대한 객체
        self.firebase = FirebaseManager() # Firebase에 대한 객체
        self.__user = None # 현재 로그인한 사용자


    def create_join_callback(self):
        """
        회원가입 콜백
        """
        @self.app.callback(
            Output('login_modal', 'is_open', allow_duplicate=True), # output
            Output('login_modal', 'children', allow_duplicate=True), # output       
            Input('joinbtn', 'n_clicks'), # btn
            State('id', 'value'), # id state
            State('pw', 'value'), # pw state
            prevent_initial_call=True # 최초 실행 방지
        )
        def join_callback(n_clicks, id, pw):
            if n_clicks and id and pw:
                try:
                    self.__user = self.firebase.auth.create_user_with_email_and_password(id, pw) # id, pw 기반의 사용자 생성
                    user_info = self.firebase.auth.get_account_info(self.__user['idToken']) # user 정보 가져오기
                    email_verified = user_info['users'][0]['emailVerified']  
                    if not email_verified: # 인증아닌 유저
                        self.firebase.auth.send_email_verification(self.__user['idToken']) # 이메일 인증 메일 전송
                    return True, [
                        dbc.ModalHeader("회원가입"),
                        dbc.ModalBody(f'{id}님 회원가입을 축하드립니다! 이메일 인증을 완료하십시오'),
                    ]
                except Exception as e:
                    return True, [
                        dbc.ModalHeader("회원가입"),
                        dbc.ModalBody(f'회원가입 실패: {str(e)}'),

                    ]
            return False, []


            
    def create_login_callback(self):
        """
        로그인 콜백
        """
        @self.app.callback(
            [Output('login_modal', 'is_open', allow_duplicate=True), # output
            Output('login_modal', 'children', allow_duplicate=True), # output      
            Output('loginbtn', 'style'), # output
            Output('joinbtn', 'style'), # output
            Output('id', 'style'), # output
            Output('pw', 'style'), # output
            Output('idlabel', 'style'), # output
            Output('pwlabel', 'style'),], # output
            Input('loginbtn', 'n_clicks'), # btn
            State('id', 'value'), # id state
            State('pw', 'value'), # pw state
            prevent_initial_call=True,

        )
        def login_callback(n_clicks, id, pw):
            if n_clicks and id and pw:
                try:
                    self.__user = self.firebase.auth.sign_in_with_email_and_password(id, pw) # id로 user 찾기
                    user_info = self.firebase.auth.get_account_info(self.__user['idToken']) # user 정보 가져오기
                    email_verified = user_info['users'][0]['emailVerified']
                    if email_verified:  # 인증 유저
                        return True, [
                        dbc.ModalHeader("로그인"),
                        dbc.ModalBody(f'{id}님 환영합니다😄'),
                    ], {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}, {'display': 'none'}
                    else:
                        return True, [
                        dbc.ModalHeader("로그인"),
                        dbc.ModalBody(f'{id}에 대한 이메일 인증을 완료하십시오'),

                    ], {}, {}, {}, {}, {}, {}
                except Exception as e:
                    return True, [
                        dbc.ModalHeader("로그인"),
                        dbc.ModalBody(f'로그인 실패: {str(e)}'),

                    ], {}, {}, {}, {}, {}, {}
                
            return False, [], {}, {}, {}, {}, {}, {}
    
    def refresh_token_callback(self):
        @self.app.callback(
            Output('interval-component', 'n_intervals'),
            Input('interval-component', 'n_intervals'),
            prevent_initial_call=True,
        )
        def update_every_30mins(n):
            self.firebase.auth.refresh(self.firebase.auth.get_account_info(self.__user['idToken']))
            print(f'{self.__user["email"]} refreshed')
            return n+1
        
    def create_logout_callback(self):
        @self.app.callback(
            [Output('login_modal', 'is_open', allow_duplicate=True), # output
            Output('login_modal', 'children', allow_duplicate=True), # output     
            Output('loginbtn', 'style', allow_duplicate=True), # output
            Output('joinbtn', 'style', allow_duplicate=True), # output
            Output('id', 'style', allow_duplicate=True), # output
            Output('pw', 'style', allow_duplicate=True), # output
            Output('idlabel', 'style', allow_duplicate=True), # output
            Output('pwlabel', 'style', allow_duplicate=True),], # output
            Input('logoutbtn', 'n_clicks'), # btn
            prevent_initial_call=True,
        )
        def logout_callback(n_clicks):
            if n_clicks:
                try:
                    self.firebase.auth.current_user = None
                    self.__user = None
                    return True, [
                        dbc.ModalHeader("로그아웃"),
                        dbc.ModalBody(f'로그아웃 되었습니다'),
                    ], {}, {}, {}, {}, {}, {}
                except Exception as e:
                    return True, [
                        dbc.ModalHeader("로그아웃"),
                        dbc.ModalBody(f'로그아웃 실패: {str(e)}'),

                    ], {}, {}, {}, {}, {}, {}
                
            return False, [], {}, {}, {}, {}, {}, {}
        
    def resources_callback():
        pass

    def carbon_emission_fig_callback():
        pass

    def gpu_freq_fig_callback():
        pass

    def carbon_density_fig_callback():
        pass

    def energy_output_fig_callback():
        pass

    def geo_callback():
        pass
