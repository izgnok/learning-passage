from dash import Dash, html, dcc, dash_table, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objects as px

external_stylesheets = ['./assets/css/style.css']  # CSS 파일명
fig = px.Figure(data=[px.Scatter(x=[1, 2, 3], y=[4, 1, 2])])

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP, external_stylesheets] )
app.title = 'Carbon friendly'
app._favicon = './assets/css/favicon/favicon.ico'
df_100_measurement = pd.read_csv("./data/100_measurement.csv")
df_90_measurement = pd.read_csv("./data/90_measurement.csv")

df_dict = {100:df_100_measurement, 90:df_90_measurement}



app.layout = html.Div([

    html.Div(className='blank'),
    #left-section
    html.Div([
        #logo section
        html.Div([html.Img(src='assets\img\icon.png', style={'padding':'0.2em'}), html.Strong("Carbon friendly")], id='logo', className='logo'),
        html.P(),

        html.Div([
            # ID, PW Input
            html.Div([
                html.Label("I D "),
                dcc.Input("아이디를 입력하세요", type='text', id='id', className='id', style={'width':'100%'}),
                html.Br(),

                html.Label("PW "),
                dcc.Input("비밀번호를 입력하세요", type='password', id='pw', className='pw', style={'width':'100%'}),
                html.Br()
            ]),

            # Button
            html.Div([
                html.Button("로그인", id='login', style={'width':'auto', 'hight':'autu'})
            ], className='login'),
        ], style={'display':'flex'}),

        html.P(),

        # Computing 
        html.Div([
            html.H1("Computing Info🖥️"),
            html.Strong(html.Label("CPU: ", className='Lcpu')),
            html.Div("Intel(R) Xeon(R) pxld 6230R CPU @ 2.10GHz", id='cpu', className='cpu', style={'display': 'inline-flex'}),
            html.Br(),

            html.Strong(html.Label("GPU: ", className='LGpu')),
            html.Div("Tesla V100 SMX 32GB", id='Gpu', className='Gpu', style={'display': 'inline-flex'}),
            html.Br(),

            html.Strong(html.Label("RAM: ", className='LRAM')),
            html.Div("128GB", id='ram', className='ram', style={'display': 'inline-flex'}),
            html.Br(),
        ], className='computing')
    ], className='left-section'), 

    
    html.Div(className='split'),

    #right-section
    html.Div([
        
        # 상단 그래프
        html.Div([
            html.Div(dcc.Graph(figure=fig),),
            html.Div(dcc.Graph(figure=fig),),
            html.Div(dcc.Graph(figure=fig),),
        ], className='top-figure'),

        # 지도
        html.Div([
            dcc.Graph(figure=fig)
        ], className='geo'),

        # 하단 그래프
        html.Div([
            html.Div([dcc.Graph(figure=fig),]),
            html.Div([dcc.Graph(figure=fig)])
        ], className='bottom-figure')

    ], className='right-section'),

    #footer
    html.Div(
            [
                html.P("© 2023 Data Science Lab All Rights Reserved."),
                html.P(
                    [
                        html.P("49315. 부산광역시 사하구 낙동대로 550번길 37(하단동) 동아대학교 공과대학1호관 4층 423호"),
                        html.A("Lab Website", href="https://www.datasciencelabs.org/", target='_blank'),
                        html.A("Contact Us", href="https://github.com/datascience-labs", target='_blank'),
                        html.A("Maker github", href="https://github.com/jhparkland", target='_blank'),
                    ]
                )
            ],
            className="footer"
        ),

], className='main')



if __name__ == '__main__':
    app.run(debug=True, port='9090')