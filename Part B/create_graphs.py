import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os
from tqdm import tqdm

start = 'C:/Users/gony/Desktop/'


def generate_graph(data, num_nodes, name, event, save):
    to_graph = data.head(num_nodes)
    G = nx.from_pandas_edgelist(to_graph, 'source', 'target', edge_attr='weight')
    pos = nx.spring_layout(G)
    edges_list, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

    # Create nodes trace
    nodes_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers',
        marker=dict(size=10, color='pink'),
        hoverinfo='skip'  # Skip hoverinfo for nodes
    )

    # Create edges trace
    edges_trace = go.Scatter(
        x=[pos[edge[0]][0] for edge in edges_list],
        y=[pos[edge[0]][1] for edge in edges_list],
        mode='lines',
        line=dict(width=1, color='gray')
    )

    # Create annotations for node names
    node_annotations = []
    for node, (x, y) in pos.items():
        annotation = dict(
            x=x,
            y=y,
            text=str(node),
            showarrow=False,
            font=dict(size=8),
            xanchor='left',
            yanchor='bottom',
            xshift=5,
            yshift=5
        )
        node_annotations.append(annotation)

    # Create figure
    fig = go.Figure(data=[edges_trace, nodes_trace])

    # Set layout options
    fig.update_layout(
        title='Interactive Graph',
        hovermode='closest',
        showlegend=False,
        width=800,
        height=600,
        annotations=node_annotations
    )

    # # Display the interactive graph
    # fig.show()

    if save:
        # Download the HTML file from Colab to your local machine
        fig.write_html(start+'data/graphs/' + event + '/' + name + ".html")

    if not save:
        return fig


if __name__ == '__main__':

    # 9/11
    path = start+'data/new/9_11_2001/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        generate_graph(data=day, num_nodes=50, name=f[5:-4]+'_graph', event='9_11_2001', save=True)

    # iraq
    path = start + 'data/new/iraq_3_20_2003/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        generate_graph(data=day, num_nodes=50, name=f[5:-4] + '_graph', event='iraq_3_20_2003', save=True)

    # hurricane katrina
    path = start + 'data/new/katrina_08_2005/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        generate_graph(data=day, num_nodes=50, name=f[5:-4] + '_graph', event='katrina_08_2005', save=True)

    # binladin_02_05_2011
    path = start + 'data/new/binladin_02_05_2011/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        generate_graph(data=day, num_nodes=50, name=f[5:-4] + '_graph', event='binladin_02_05_2011', save=True)

    # boston marathon attack
    path = start + 'data/new/boston_15_04_2013/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        generate_graph(data=day, num_nodes=50, name=f[5:-4] + '_graph', event='boston_15_04_2013', save=True)
