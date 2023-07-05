import pandas as pd
import networkx as nx
import community as community_louvain
import time
import os


def weighted_degree_centrality(graph):
    weighted_degrees = {}
    for node in graph.nodes:
        weighted_degree = sum(weight for _, _, weight in graph.edges(node, data='weight'))
        weighted_degrees[node] = weighted_degree
    return weighted_degrees


def centrality_metrics(graph):
    """
    Calculates centrality metrics of a graph.
    Parameters: graph (networkx.Graph): The input graph.
    Returns: dict: dictionaries for the different metrics in the following order:
                    degree_centrality, betweenness_centrality, closeness_centrality, eigenvector_centrality
    """
    start_time = time.time()
    degree_centrality = weighted_degree_centrality(G)
    print('degree: ', time.time() - start_time)
    start_time = time.time()

    start_time = time.time()
    eigenvector_centrality = nx.eigenvector_centrality(graph, weight='weight')
    print('eigenvector: ', time.time() - start_time)

    cent_df = pd.DataFrame(columns=['node', 'degree_cent', 'eigenvector_cent'])
    for node in eigenvector_centrality.keys():
        degree = degree_centrality[node]
        eigenvector = eigenvector_centrality[node]
        cent_df.loc[len(cent_df)] = [node, degree, eigenvector]

    return cent_df


def find_communities(graph):
    # Apply the Louvain algorithm to detect communities
    partition = community_louvain.best_partition(graph)

    # Create a dictionary to store communities
    communities = {}

    # Iterate over nodes and their corresponding communities
    for node, community_id in partition.items():
        if community_id not in communities:
            communities[community_id] = []
        communities[community_id].append(node)

    # Calculate the community density for each community
    community_density = {}
    for community_id, community in communities.items():
        community_subgraph = graph.subgraph(community)
        internal_edges = community_subgraph.number_of_edges()
        total_edges = nx.density(community_subgraph) * nx.number_of_edges(community_subgraph)
        if total_edges == 0:
            print(community_id)
            community_density[community_id] = 0
        else:
            community_density[community_id] = internal_edges / total_edges

    # Return the communities and their density
    return list(communities.values()), community_density


def community_centrality_df(G, cent_df):
    communities, community_density = find_communities(G)
    communities_df = pd.DataFrame(columns=['id', 'nodes', 'density'])
    for i, community in enumerate(communities):
        communities_df.loc[len(communities_df)] = [i + 1, community, community_density[i]]
    top_degree = []
    for i, row in communities_df.iterrows():
        nodes = row['nodes']
        temp = pd.DataFrame(columns=['nodes', 'deg_cent'])
        for w in nodes:
            if w in cent_df['node']:
                temp.loc[len(temp)] = [w, cent_df[cent_df['node'] == w]['degree_cent'].values[0]]
            else:
                temp.loc[len(temp)] = [w, 0]
        temp.sort_values(['deg_cent'], ascending=False, inplace=True)
        top_degree.append(temp[:10].nodes.values)

    communities_df['top_degree_cent'] = top_degree
    return communities_df


start = 'C:/Users/gony/Desktop/'

# 9/11
# for f in os.listdir(start + 'data/nodes - Copy/9_11_2001/'):
#     print(f)
#     data = pd.read_csv(start + 'data/nodes - Copy/9_11_2001/' + f)
#     G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
#     cent_df = centrality_metrics(G)
#     cent_df.to_csv(start + 'data/nodes_centrality_9_11_2001/centrality_' + f[5:])
#     community_centrality_df(G, cent_df).to_csv(start + 'data/nodes_centrality_9_11_2001/centrality_community_' + f[5:])
#
# # IRAQ
# for f in os.listdir(start + 'data/nodes - Copy/iraq_3_20_2003/'):
#     print(f)
#     data = pd.read_csv(start + 'data/nodes - Copy/iraq_3_20_2003/' + f)
#     G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
#     cent_df = centrality_metrics(G)
#     cent_df.to_csv(start + 'data/nodes_centrality_iraq_3_20_2003/centrality_' + f[5:])
#     community_centrality_df(G, cent_df).to_csv(start + 'data/nodes_centrality_iraq_3_20_2003/centrality_community_' + f[5:])
#
# # KATRINA
# for f in os.listdir(start + 'data/nodes - Copy/katrina_08_2005/'):
#     print(f)
#     data = pd.read_csv(start + 'data/nodes - Copy/katrina_08_2005/' + f)
#     G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
#     cent_df = centrality_metrics(G)
#     cent_df.to_csv(start + 'data/nodes_centrality_katrina_08_2005/centrality_' + f[5:])
#
#     community_centrality_df(G, cent_df).to_csv(start + 'data/nodes_centrality_katrina_08_2005/centrality_community_' + f[5:])

# BIN LADEN
for f in os.listdir(start + 'data/nodes - Copy/binladin_02_05_2011/'):
    print(f)
    data = pd.read_csv(start + 'data/nodes - Copy/binladin_02_05_2011/' + f)
    G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
    cent_df = centrality_metrics(G)
    cent_df.to_csv(start + 'data/nodes_centrality_binladin_02_05_2011/centrality_' + f[5:])
    community_centrality_df(G, cent_df).to_csv(start + 'data/nodes_centrality_binladin_02_05_2011/centrality_community_' + f[5:])

# BOSTON
for f in os.listdir(start + 'data/nodes - Copy/boston_15_04_2013/'):
    print(f)
    data = pd.read_csv(start + 'data/nodes - Copy/boston_15_04_2013/' + f)
    G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
    cent_df = centrality_metrics(G)
    cent_df.to_csv(start + 'data/nodes_centrality_boston_15_04_2013/centrality_' + f[5:])
    community_centrality_df(G, cent_df).to_csv(start + 'data/nodes_centrality_boston_15_04_2013/centrality_community_' + f[5:])
