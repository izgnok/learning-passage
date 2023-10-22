from dash import Dash, dcc, html # Dash components
from module.App.callback import * # callback functions
from module.App.layout import * # layout functions
import dash_bootstrap_components as dbc # bootstrap components

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP]) # bootstrap theme
app.title = 'Carbon friendly' # app title
app._favicon = 'assets/favicon/favicon.ico' # app favicon
server = app.server # heroku server connection

# create layout
layout = AppLayout(app) 
app.layout = layout.create_layout()

# create callback

if __name__ == "__main__":
    app.run(debug=True)
    app.run_server()