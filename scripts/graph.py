import os, sys
import networkx as nx
import csv
import pandas as pd
import matplotlib.pyplot as plt
from netgraph import Graph

def to_vector(tuple_list):
    sorted_list = sorted(tuple_list.items())
    return [item for _, item in sorted_list]

sys.setrecursionlimit(9999) # Only to test the visualization

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
filepath = os.path.join(root_dir, '.\data\graph\graph_connections.csv')

data = open(filepath, "r")
next(data, None)
Graphtype = nx.Graph()

G = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float),))

degree_centrality = G.degree(weight='weight')
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
communities = nx.community.asyn_lpa_communities(G, weight='weight')
triangles = nx.triangles(G)
clustering = nx.clustering(G, weight='weight')
# average_clustering = nx.average_clustering(G, weight='weight')

node_to_community = dict()
for index, community in enumerate(communities):
    for vertex in community:
        node_to_community[vertex] = index

data_dict = {'node': [i for i in range(1,1001)]}

sorted_degrees = sorted(degree_centrality)
data_dict['degree'] = [degree for _, degree in sorted_degrees]

data_dict['closeness'] = to_vector(closeness_centrality)
data_dict['betweenness'] = to_vector(betweenness_centrality)
data_dict['community'] = to_vector(node_to_community)
data_dict['triangles'] = to_vector(triangles)
data_dict['clustering'] = to_vector(clustering)

df = pd.DataFrame(data_dict).set_index('node')
df.to_csv(os.path.join(root_dir, '.\data\graph\metrics.csv'))


# This is the code for testing the graph visualization (not working for now)
# By switching to the default NetworkX draw function, it works, but it can't display the communities
community_to_color = {
    0 : 'tab:blue',
    1 : 'tab:orange',
    2 : 'tab:green',
    3 : 'tab:red',
    4 : 'tab:yellow',
    5 : 'tab:pink',
    6 : 'tab:purple',
}

node_color = {node: community_to_color[community_id] for node, community_id in node_to_community.items()}

# Graph(G,
#       node_color=node_color, node_edge_width=0, edge_alpha=0.1,
#       node_layout='community', node_layout_kwargs=dict(node_to_community=node_to_community),
#       edge_layout='bundled', edge_layout_kwargs=dict(k=2000),
# )

#plt.show()
