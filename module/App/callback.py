from dash import Dash, dcc, html
from module.App.layout import LayoutManager
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objs as go

class CallbackManager:
    """
    앱 콜백 스켈레톤 정의
    """

    def __init__(self, app):
        self.app = app

    def create_login_callback():
        pass

    def create_resources_callback():
        pass

    def create_graph_callback():
        pass

    def create_geo_callback():
        pass
