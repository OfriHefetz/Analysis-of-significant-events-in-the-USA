import dash
from dash import dcc, callback, Output, Input, dash_table
from dash import html
import pandas as pd
from create_graphs import generate_graph
import plotly.io as pio
import json
import re

start = 'C:/Users/gony/Desktop/data/'

dates_9_11 = [f'{i}.09.2001' for i in range(6, 27)]
dates_iraq = [f'{i}.03.2003' for i in range(18, 32)] + [f'{i}.04.2003' for i in range(1, 4)]
dates_katrina = [f'{i}.08.2005' for i in range(18, 32)] + [f'{i}.09.2005' for i in range(1, 7)]
dates_binladin = [f'{i}.04.2011' for i in range(27, 31)] + [f'{i}.05.2011' for i in range(1, 18)]
dates_boston = [f'{i}.04.2013' for i in range(11, 31)]

df = pd.read_csv(start + 'nodes_centrality_9_11_2001/centrality_community_6.09.2001.csv')
df.sort_values(['density'], ascending=False, inplace=True)
df = df[['id', 'top_degree_cent']][:10]


def read_html(path):
    with open(path) as f:
        temp = f.read()
    call_arg_str = re.findall(r'Plotly\.newPlot\((.*)\)', temp[-2 ** 16:])[0]
    call_args = json.loads(f'[{call_arg_str}]')
    plotly_json = {'data': call_args[1], 'layout': call_args[2]}
    return pio.from_json(json.dumps(plotly_json))


def generate_table(dataframe, name, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])


fig_9_11 = read_html(start + 'graphs/9_11_2001/6.09.2001_graph.html')
fig_iraq = read_html(start + 'graphs/iraq_3_20_2003/18.03.2003_graph.html')
fig_katrina = read_html(start + 'graphs/katrina_08_2005/2.08.2005_graph.html')
fig_binladin = read_html(start + 'graphs/binladin_02_05_2011/1.05.2011_graph.html')
fig_boston = read_html(start + 'graphs/boston_15_04_2013/11.04.2013_graph.html')

app = dash.Dash(__name__)
app.layout = html.Div(
    children=[
        html.H1(children="Analyzing Graphs", ),
        html.P(
            children="Analyzing graphs per day",
        ),
        html.H2(children='graphs for the event of 9/11 terror attack'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_9_11'),
        html.H3(children=dates_9_11[0], id='title_9_11'),
        html.Div([html.Div(dcc.Graph(
                            figure=fig_9_11,
                            id='graph_9_11'),
                            style={'width': '45%', 'display': 'inline-block'}),
                    html.Div(dash_table.DataTable(
                            id='table-container',
                            columns=[{"name": i, "id": i} for i in df],
                            data=df.to_dict('records'), style_table={'height': 200, 'overflowX': 'auto'},
                ), style={'width': '45%', 'display': 'inline-block'})]),
        html.H2(children='graphs for the event of invading Iraq at March 2003'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_iraq'),
        html.H3(children=dates_iraq[0], id='title_iraq'),
        dcc.Graph(
            figure=fig_iraq,
            id='graph_iraq',
        ),
        html.H2(children='graphs for the event of Hurrican Katrina at August 2005'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_katrina'),
        html.H3(children=dates_katrina[0], id='title_katrina'),
        dcc.Graph(
            figure=fig_katrina,
            id='graph_katrina',
        ),
        html.H2(children='graphs for the event of the killing of Bin Laden at May 2011'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_binladin'),
        html.H3(children=dates_binladin[0], id='title_binladin'),
        dcc.Graph(
            figure=fig_binladin,
            id='graph_binladin',
            # title=dates_binladin[1],
        ),
        html.H2(children='graphs for the Boston Marathon Booming at April 2013'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_boston'),
        html.H3(children=dates_boston[0], id='title_boston'),
        dcc.Graph(
            figure=fig_boston,
            id='graph_boston',
            # title=dates_boston[1,]
        ),
    ]
)


@callback(
    Output(component_id='graph_9_11', component_property='figure'),
    Output(component_id='title_9_11', component_property='children'),
    Output(component_id='table-container', component_property='data'),
    Input(component_id='range-slider_9_11', component_property='value'),

)
def update_9_11_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/9_11_2001/{dates_9_11[val_chosen]}_graph.html'
    fig = read_html(path)
    df = pd.read_csv(start + f'nodes_centrality_9_11_2001/centrality_community_{dates_9_11[val_chosen]}.csv')
    df.sort_values(['density'], ascending=False, inplace=True)
    df = df[['id', 'top_degree_cent']][:10]
    return fig, dates_9_11[val_chosen], df.to_dict('records'),


@callback(
    Output(component_id='graph_iraq', component_property='figure'),
    Output(component_id='title_iraq', component_property='children'),
    Input(component_id='range-slider_iraq', component_property='value')
)
def update_iraq_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/iraq_3_20_2003/{dates_iraq[val_chosen]}_graph.html'
    fig = read_html(path)
    return fig, dates_iraq[val_chosen]


@callback(
    Output(component_id='graph_katrina', component_property='figure'),
    Output(component_id='title_katrina', component_property='children'),
    Input(component_id='range-slider_katrina', component_property='value')
)
def update_katrina_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/katrina_08_2005/{dates_katrina[val_chosen]}_graph.html'
    fig = read_html(path)
    return fig, dates_katrina[val_chosen]


@callback(
    Output(component_id='graph_binladin', component_property='figure'),
    Output(component_id='title_binladin', component_property='children'),
    Input(component_id='range-slider_binladin', component_property='value')
)
def update_binladin_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/binladin_02_05_2011/{dates_binladin[val_chosen]}_graph.html'
    fig = read_html(path)
    return fig, dates_binladin[val_chosen]


@callback(
    Output(component_id='graph_boston', component_property='figure'),
    Output(component_id='title_boston', component_property='children'),
    Input(component_id='range-slider_boston', component_property='value')
)
def update_boston_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}data/graphs/boston_15_04_2013/{dates_boston[val_chosen]}_graph.html'
    fig = read_html(path)
    return fig, dates_boston[val_chosen]


if __name__ == "__main__":
    app.run_server(debug=True)
