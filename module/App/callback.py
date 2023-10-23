from dash import Dash, dcc, html, Output, Input, State
from module.Firebase.firebase import FirebaseManager
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

class CallbackManager:
    """
    앱 콜백 스켈레톤 정의
    """

    def __init__(self, app):
        self.app = app # Dash에 대한 객체
        self.firebase = FirebaseManager() # Firebase에 대한 객체

    def create_join_callback(self):
        """
        회원가입 콜백
        """
        @self.app.callback(
            Output('sing_up_info', 'children'), # output
            Input('joinbtn', 'n_clicks'), # btn
            State('id', 'value'), # id state
            State('pw', 'value'), # pw state
            prevent_initial_call=True # 최초 실행 방지
        )
        def join_callback(n_clicks, id, pw):
            if n_clicks and id and pw:
                try:
                    user_record = self.firebase.auth.create_user(
                        email=id,
                        password=pw,
                        email_verified=True,
                    )
                    return f'{id}님 회원가입을 환영합니다!'
                except Exception as e:
                    return f'회원가입 실패: {str(e)}'
            return ' '

            
    def create_login_callback(self):
        """
        로그인 콜백
        """
        @self.app.callback(
            Output('login_info', 'children'), # output
            Input('loginbtn', 'n_clicks'), # btn
            State('id', 'value'), # id state
            State('pw', 'value'), # pw state
        )
        def login_callback(n_clicks, id, pw):
            if n_clicks and id and pw:
                try:
                    user = self.firebase.auth.get_user_by_email(id) # id로 user 찾기
                    return f'{user.uid}님 환영합니다!'
                except Exception as e:
                    return f'로그인 실패: {str(e)}'
    def resources_callback():
        pass

    def graph_callback():
        pass

    def geo_callback():
        pass
