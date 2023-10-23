from dash import Dash, dcc, html # Dash components
from module.App.callback import CallbackManager # callback functions
from module.App.layout import LayoutManager # layout functions
import dash_bootstrap_components as dbc # bootstrap components

app = Dash(__name__, 
           external_stylesheets=[dbc.themes.BOOTSTRAP], 
           external_scripts = ['\\module\\Firebase\\firebase_sdk.html',
                               'https://www.gstatic.com/firebasejs/8.0.0/firebase-app.js',
                               'https://www.gstatic.com/firebasejs/8.0.0/firebase-auth.js',]) # bootstrap theme

app.title = 'Carbon friendly' # app title
app._favicon = 'assets/favicon/favicon.ico' # app favicon
server = app.server # heroku server connection

# create layout
layout = LayoutManager(app) 
app.layout = layout.create_layout()

# create callback
callback = CallbackManager(app)

callback.create_join_callback() # 회원가입 콜백
callback.create_login_callback() # 로그인 콜백
if __name__ == "__main__":
    app.run(debug=True)
    #app.run_server()