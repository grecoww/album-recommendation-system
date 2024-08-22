import os, sys
import networkx as nx
import csv
import pandas as pd
import matplotlib.pyplot as plt
from graph_query import get_info_by_node

def to_vector(tuple_list):
    sorted_list = sorted(tuple_list.items())
    return [item for _, item in sorted_list]

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
filepath = os.path.join(root_dir, '.\data\graph\graph_connections.csv')

data = open(filepath, "r")
next(data, None)
Graphtype = nx.Graph()

G = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float), ('reverse_weight', float)))

degree_centrality = G.degree(weight='weight')
average_path_length = nx.average_shortest_path_length(G, weight='reverse_weight')
closeness_centrality = nx.closeness_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight='reverse_weight')
communities = nx.community.louvain_communities(G, weight='weight', resolution=2)
triangles = nx.triangles(G)
clustering = nx.clustering(G, weight='weight')
average_clustering = nx.average_clustering(G, weight='weight')

print(f"Average path length: {average_path_length}")
communities_filename = os.path.join(root_dir, '.\data\graph\general_metrics.txt')
with open(communities_filename, 'w', encoding='utf-8') as f:
    print(f"Average clustering: {average_clustering}", end='\n\n', file=f)
    print("Communities:", file=f)
    for index, community in enumerate(communities):
        print(index, file=f)
        print(get_info_by_node(community, ['genre', 'second_genre', 'artist','descriptor']), end='\n\n', file=f)

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

# nx.draw_networkx(G, with_labels=False, node_size=4)
# plt.show()