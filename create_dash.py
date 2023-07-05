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

community_9_11 = pd.read_csv(start + 'nodes_centrality_9_11_2001/centrality_community_6.09.2001.csv')
community_9_11.sort_values(['density'], ascending=False, inplace=True)
community_9_11 = community_9_11[['id', 'top_degree_cent']][:10]

community_iraq = pd.read_csv(start + 'nodes_centrality_iraq_3_20_2003/centrality_community_1.04.2003.csv')
community_iraq.sort_values(['density'], ascending=False, inplace=True)
community_iraq = community_iraq[['id', 'top_degree_cent']][:10]

community_katrina = pd.read_csv(start + 'nodes_centrality_katrina_08_2005/centrality_community_1.09.2005.csv')
community_katrina.sort_values(['density'], ascending=False, inplace=True)
community_katrina = community_katrina[['id', 'top_degree_cent']][:10]

community_bin_laden = pd.read_csv(start + 'nodes_centrality_binladin_02_05_2011/centrality_community_1.05.2011.csv')
community_bin_laden.sort_values(['density'], ascending=False, inplace=True)
community_bin_laden = community_bin_laden[['id', 'top_degree_cent']][:10]

community_boston = pd.read_csv(start + 'nodes_centrality_boston_15_04_2013/centrality_community_11.04.2013.csv')
community_boston.sort_values(['density'], ascending=False, inplace=True)
community_boston = community_boston[['id', 'top_degree_cent']][:10]

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
        html.H1(children="Analyzing Results", ),
        # html.P(
        #     children="Analyzing graphs per day",
        # ),
        html.H2(children='Analysing results of 9/11 terror attack'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_9_11'),
        html.H3(children=dates_9_11[0], id='title_9_11'),
        html.H3(children='top 10 nodes with size based on degree centrality'),
        html.Div(dcc.Graph(
                            figure=fig_9_11,
                            id='graph_9_11'),
                            style={'width': '45%', 'display': 'inline-block'}),
        html.H3(children='top 10 communities based on density and the top 20 nodes based on degree centrality'),
        html.Div(dash_table.DataTable(
                            id='table-9_11',
                            columns=[{"name": i, "id": i} for i in community_9_11],
                            data=community_9_11.to_dict('records'), style_table={'height': 200, 'overflowX': 'auto'},
                ), style={'width': '45%', 'display': 'inline-block'}),

        html.H2(children='Analysing results of Iraq invation'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_iraq'),
        html.H3(children=dates_iraq[0], id='title_iraq'),
        html.H3(children='top 10 nodes with size based on degree centrality'),
        html.Div(dcc.Graph(
                            figure=fig_iraq,
                            id='graph_iraq'),
                            style={'width': '45%', 'display': 'inline-block'}),
        html.H3(children='top 10 communities based on density and the top 20 nodes based on degree centrality'),
        html.Div(dash_table.DataTable(
                            id='table-iraq',
                            columns=[{"name": i, "id": i} for i in community_iraq],
                            data=community_iraq.to_dict('records'), style_table={'height': 200, 'overflowX': 'auto'},
                ), style={'width': '45%', 'display': 'inline-block'}),

        html.H2(children='Analysing results of Hurrican Katrina'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_katrina'),
        html.H3(children=dates_katrina[0], id='title_katrina'),
        html.H3(children='top 10 nodes with size based on degree centrality'),
        html.Div(dcc.Graph(
            figure=fig_katrina,
            id='graph_katrina'),
                            style={'width': '45%', 'display': 'inline-block'}),
        html.H3(children='top 10 communities based on density and the top 20 nodes based on degree centrality'),
        html.Div(dash_table.DataTable(
            id='table-katrina',
            columns=[{"name": i, "id": i} for i in community_katrina],
            data=community_katrina.to_dict('records'), style_table={'height': 200, 'overflowX': 'auto'},
                ), style={'width': '45%', 'display': 'inline-block'}),

        html.H2(children='Analysing results of the killing of Bin Laden'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_binladin'),
        html.H3(children=dates_binladin[0], id='title_binladin'),
        html.H3(children='top 10 nodes with size based on degree centrality'),
        html.Div(dcc.Graph(
            figure=fig_binladin,
            id='graph_binladin'),
                            style={'width': '45%', 'display': 'inline-block'}),
        html.H3(children='top 10 communities based on density and the top 20 nodes based on degree centrality'),
        html.Div(dash_table.DataTable(
            id='table-binladin',
            columns=[{"name": i, "id": i} for i in community_bin_laden],
            data=community_bin_laden.to_dict('records'), style_table={'height': 200, 'overflowX': 'auto'},
                ), style={'width': '45%', 'display': 'inline-block'}),

        html.H2(children='Analysing results of the Boston Marathon Booming'),
        dcc.RangeSlider(-5, 15, 1, value=[-5], id='range-slider_boston'),
        html.H3(children=dates_boston[0], id='title_boston'),
        html.H3(children='top 10 nodes with size based on degree centrality'),
        html.Div(dcc.Graph(
            figure=fig_boston,
            id='graph_boston'),
            style={'width': '45%', 'display': 'inline-block'}),
        html.H3(children='top 10 communities based on density and the top 20 nodes based on degree centrality'),
        html.Div(dash_table.DataTable(
            id='table-boston',
            columns=[{"name": i, "id": i} for i in community_boston],
            data=community_boston.to_dict('records'), style_table={'height': 200, 'overflowX': 'auto'},
        ), style={'width': '45%', 'display': 'inline-block'}),

    ]
)


@callback(
    Output(component_id='graph_9_11', component_property='figure'),
    Output(component_id='title_9_11', component_property='children'),
    Output(component_id='table-9_11', component_property='data'),
    Input(component_id='range-slider_9_11', component_property='value'),

)
def update_9_11_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/9_11_2001/{dates_9_11[val_chosen]}_graph.html'
    fig = read_html(path)
    df = pd.read_csv(start + f'nodes_centrality_9_11_2001/centrality_community_{dates_9_11[val_chosen]}.csv')
    df.sort_values(['density'], ascending=False, inplace=True)
    df = df[['id', 'top_degree_cent']][:10]
    return fig, dates_9_11[val_chosen], df.to_dict('records')


@callback(
    Output(component_id='graph_iraq', component_property='figure'),
    Output(component_id='title_iraq', component_property='children'),
    Output(component_id='table-iraq', component_property='data'),
    Input(component_id='range-slider_iraq', component_property='value'),

)
def update_iraq_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/iraq_3_20_2003/{dates_iraq[val_chosen]}_graph.html'
    fig = read_html(path)
    df = pd.read_csv(start + f'nodes_centrality_iraq_3_20_2003/centrality_community_{dates_iraq[val_chosen]}.csv')
    df.sort_values(['density'], ascending=False, inplace=True)
    df = df[['id', 'top_degree_cent']][:10]
    return fig, dates_iraq[val_chosen], df.to_dict('records')


@callback(
    Output(component_id='graph_katrina', component_property='figure'),
    Output(component_id='title_katrina', component_property='children'),
    Output(component_id='table-katrina', component_property='data'),
    Input(component_id='range-slider_katrina', component_property='value'),

)
def update_katrina_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/katrina_08_2005/{dates_katrina[val_chosen]}_graph.html'
    fig = read_html(path)
    df = pd.read_csv(start + f'nodes_centrality_katrina_08_2005/centrality_community_{dates_katrina[val_chosen]}.csv')
    df.sort_values(['density'], ascending=False, inplace=True)
    df = df[['id', 'top_degree_cent']][:10]
    return fig, dates_katrina[val_chosen], df.to_dict('records')

@callback(
    Output(component_id='graph_binladin', component_property='figure'),
    Output(component_id='title_binladin', component_property='children'),
    Output(component_id='table-binladin', component_property='data'),
    Input(component_id='range-slider_binladin', component_property='value'),

)
def update_binladin_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/binladin_02_05_2011/{dates_binladin[val_chosen]}_graph.html'
    fig = read_html(path)
    df = pd.read_csv(start + f'nodes_centrality_binladin_02_05_2011/centrality_community_{dates_binladin[val_chosen]}.csv')
    df.sort_values(['density'], ascending=False, inplace=True)
    df = df[['id', 'top_degree_cent']][:10]
    return fig, dates_binladin[val_chosen], df.to_dict('records')


@callback(
    Output(component_id='graph_boston', component_property='figure'),
    Output(component_id='title_boston', component_property='children'),
    Output(component_id='table-boston', component_property='data'),
    Input(component_id='range-slider_boston', component_property='value'),

)
def update_boston_graph(val_chosen):
    val_chosen = val_chosen[0] + 5
    path = f'{start}graphs/boston_15_04_2013/{dates_boston[val_chosen]}_graph.html'
    fig = read_html(path)
    df = pd.read_csv(start + f'nodes_centrality_boston_15_04_2013/centrality_community_{dates_boston[val_chosen]}.csv')
    df.sort_values(['density'], ascending=False, inplace=True)
    df = df[['id', 'top_degree_cent']][:10]
    return fig, dates_boston[val_chosen], df.to_dict('records')


if __name__ == "__main__":
    app.run_server(debug=True)
