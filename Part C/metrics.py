import pandas as pd
import networkx as nx
import time
import os

def centrality_metrics(graph):
    """
    Calculates centrality metrics of a graph.
    Parameters: graph (networkx.Graph): The input graph.
    Returns: dict: dictionaries for the different metrics in the following order:
                    degree_centrality, betweenness_centrality, closeness_centrality, eigenvector_centrality
    """
    start_time = time.time()
    degree_centrality = nx.degree_centrality(graph)
    print('degree: ', time.time()-start_time)
    start_time = time.time()

    # betweenness_centrality = nx.betweenness_centrality(graph)
    # print('betweenness: ', time.time() - start_time)
    # start_time = time.time()
    betweenness_centrality = 0

    closeness_centrality = nx.closeness_centrality(graph)
    print('closeness: ', time.time() - start_time)

    start_time = time.time()
    eigenvector_centrality = nx.eigenvector_centrality(graph)
    print('eigenvector: ', time.time() - start_time)

    cent_df = pd.DataFrame(columns=['node', 'degree_cent', 'closeness_cent', 'eigenvector_cent'])
    for node in degree_centrality.keys():
        degree = degree_centrality[node]
        closeness = closeness_centrality[node]
        eigenvector = eigenvector_centrality[node]
        cent_df.loc[len(cent_df)] = [node, degree, closeness, eigenvector]
    return cent_df


start = 'C:/Users/gony/Desktop/'

# for f in os.listdir(start+'data/new/9_11_2001/'):
    # print(f)
    # data = pd.read_csv(start+'data/new/9_11_2001/'+f)
    # G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
    # cent_df = centrality_metrics(G)
    # cent_df.to_csv(start+'data/nodes/9_11_2001/centrality_'+f[5:])

for f in os.listdir(start+'data/new/iraq_3_20_2003/'):
    if not os.path.exists(start+'data/nodes/iraq_3_20_2003/centrality_'+f[5:]):
        print(f)
        data = pd.read_csv(start+'data/new/iraq_3_20_2003/'+f)
        G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
        cent_df = centrality_metrics(G)
        cent_df.to_csv(start+'data/nodes/iraq_3_20_2003/centrality_'+f[5:])
#
# for f in os.listdir(start+'data/new/katrina_08_2005/'):
#     print(f)
#     data = pd.read_csv(start+'data/new/katrina_08_2005/'+f)
#     G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
#     cent_df = centrality_metrics(G)
#     cent_df.to_csv(start+'data/nodes/katrina_08_2005/centrality_'+f[5:])

# for f in os.listdir(start+'data/new/binladin_02_05_2011/'):
#     if not os.path.exists(start + 'data/new/binladin_02_05_2011/' + f):
#         print(f)
#         data = pd.read_csv(start+'data/new/binladin_02_05_2011/'+f)
#         G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
#         cent_df = centrality_metrics(G)
#         cent_df.to_csv(start+'data/nodes/binladin_02_05_2011/centrality_'+f[5:])
#
# for f in os.listdir(start+'data/new/boston_15_04_2013/'):
#     print(f)
#     data = pd.read_csv(start+'data/new/boston_15_04_2013/'+f)
#     G = nx.from_pandas_edgelist(data, 'source', 'target', edge_attr='weight')
#     cent_df = centrality_metrics(G)
#     cent_df.to_csv(start+'data/nodes/boston_15_04_2013/centrality_'+f[5:])