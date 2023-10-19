# 100_measurement.csv
from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import plotly.graph_objects as go


app = Dash(__name__)

df_100_measurement = pd.read_csv("100_measurement.csv")
df_90_measurement = pd.read_csv("90_measurement.csv")

df_dict = {100:df_100_measurement, 90:df_90_measurement}

horizontal_layout_style = {
    'display': 'flex',
    'flexDirection': 'row',  # 수평으로 배치
    'justifyContent': 'space-between',  # 요소들을 좌우로 분산 배치
}

app.layout = html.Div([
    html.H1("딥러닝 학습시 주파수에 따른 성능지표"),
    html.Label('주파수 선정'),
    dcc.Slider(max = 100, 
               min = 50, 
               step=10, 
               value=100, 
               id='measurement', 
               marks={i: str(i) for i in range(50, 101, 10)},  # 슬라이더의 눈금 표시
               tooltip={'placement': 'bottom', 'always_visible': True}),  # 툴팁 표시 설정), # 100 ~ 50 까지 10 단위로

    html.H1(id='title'),
    html.H2('temp', id='temp'),

    html.Div(style = horizontal_layout_style, children = [
        dcc.Graph(id='graph1'),
        dcc.Graph(id='graph2'),
        dcc.Graph(id='graph3'),
        dcc.Graph(id='graph4'),
    ], className='row'),

    dcc.Graph(figure=go.Figure(go.Indicator(
    mode = "gauge+number",
    value = 450,
    title = {'text': "Speed"},
    domain = {'x': [0, 1], 'y': [0, 1]}
))) 

 

])

@app.callback(
    Output('title', 'children'),
    Input('measurement', 'value')
)
def update_table(value):
    if value < 90:
        return html.H2("수집중..")
    else:
        return f'{value}_measurement VGGNet', \
            dash_table.DataTable(
            data= df_dict[int(f'{value}')]
            .reset_index()
            .drop(['OtimalCoreFreq', 'index'], axis=1)
            .to_dict('records'), 
            page_size=20, 
            id='table'
        ), \
            html.P(), \
            html.H3("Describe"), \
            dash_table.DataTable(
            data= pd.read_csv(f"{value}_measurement.csv")
            .drop(['OtimalCoreFreq', 'EpcohIdx', 'IterIdx'], axis=1)
            .describe()
            .reset_index()
            .to_dict('records'), 
            page_size=20, 
            id='describe_table'
            )



if __name__ == '__main__':
    app.run(debug=True)