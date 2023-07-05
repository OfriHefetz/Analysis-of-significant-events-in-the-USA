import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
import os
from tqdm import tqdm

start = 'C:/Users/gony/Desktop/data/'


def generate_graph(data, node_sizes_df, num_nodes, name, event, save):
    to_graph = data.head(num_nodes)
    G = nx.from_pandas_edgelist(to_graph, 'source', 'target', edge_attr='weight')
    pos = nx.spring_layout(G)
    edges_list, weights = zip(*nx.get_edge_attributes(G, 'weight').items())

    graph_nodes = G.nodes()
    filtered_node_sizes_df = node_sizes_df[node_sizes_df['node'].isin(graph_nodes)]
    # Extract node names and sizes from the filtered dataframe
    node_names = filtered_node_sizes_df['node'].tolist()
    node_sizes = filtered_node_sizes_df['degree_cent'].tolist()

    # Create a dictionary to map node names to sizes
    node_sizes_dict = dict(zip(node_names, node_sizes))

    # Define a scaling factor for node sizes
    scaling_factor = 0.02  # Adjust the scaling factor as needed

    # Create nodes trace
    nodes_trace = go.Scatter(
        x=[pos[node][0] for node in G.nodes()],
        y=[pos[node][1] for node in G.nodes()],
        mode='markers',
        marker=dict(
            size=[node_sizes_dict.get(node, 10) * scaling_factor for node in G.nodes()],
            color='pink'
        ),
        hoverinfo='skip'
    )

    # # Create edges trace
    # edges_trace = go.Scatter(
    #     x=[pos[edge[0]][0] for edge in edges_list],
    #     y=[pos[edge[0]][1] for edge in edges_list],
    #     mode='lines',
    #     line=dict(width=1, color='gray')
    # )
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
        fig.write_html(start + 'graphs/' + event + '/' + name + ".html")

    if not save:
        return fig


if __name__ == '__main__':

    # 9/11
    path = start + 'nodes - Copy/9_11_2001/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        cent_df = pd.read_csv(start + 'nodes_centrality_9_11_2001/centrality_' + f[5:])
        generate_graph(data=day, node_sizes_df=cent_df, num_nodes=50, name=f[5:-4] + '_graph', event='9_11_2001',
                       save=True)

    # iraq
    path = start + 'nodes - Copy/iraq_3_20_2003/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        cent_df = pd.read_csv(start + 'nodes_centrality_iraq_3_20_2003/centrality_' + f[5:])
        generate_graph(data=day, node_sizes_df=cent_df, num_nodes=50, name=f[5:-4] + '_graph', event='iraq_3_20_2003',
                       save=True)
    # hurricane katrina
    path = start + 'nodes - Copy/katrina_08_2005/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        cent_df = pd.read_csv(start + 'nodes_centrality_katrina_08_2005/centrality_' + f[5:])
        generate_graph(data=day, node_sizes_df=cent_df, num_nodes=50, name=f[5:-4] + '_graph', event='katrina_08_2005',
                       save=True)
    # binladin_02_05_2011
    path = start + 'nodes - Copy/binladin_02_05_2011/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        cent_df = pd.read_csv(start + 'nodes_centrality_binladin_02_05_2011/centrality_' + f[5:])
        generate_graph(data=day, node_sizes_df=cent_df, num_nodes=50, name=f[5:-4] + '_graph', event='binladin_02_05_2011',
                       save=True)
    # boston marathon attack
    path = start + 'nodes - Copy/boston_15_04_2013/'
    for f in tqdm(os.listdir(path)):
        day = pd.read_csv(path + f)
        day.sort_values('weight', ascending=False, inplace=True)
        day.reset_index(drop=False, inplace=True)
        cent_df = pd.read_csv(start + 'nodes_centrality_boston_15_04_2013/centrality_' + f[5:])
        generate_graph(data=day, node_sizes_df=cent_df, num_nodes=50, name=f[5:-4] + '_graph', event='boston_15_04_2013',
                       save=True)