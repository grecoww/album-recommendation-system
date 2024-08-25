import os
import networkx as nx
import pandas as pd
from graph_query import get_album_by_node

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
graph_path = os.path.join(root_dir, 'data', 'graph', 'graph_connections.csv')

with open(graph_path, "r") as data:
    next(data, None)
    Graphtype = nx.Graph()
    G = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float), ('reverse_weight', float)))

communities = nx.community.louvain_communities(G, weight='weight', resolution=3, seed=72)

node_to_community = dict()
for index, community in enumerate(communities):
    for vertex in community:
        node_to_community[vertex] = index

def node_list_albums(node_list):
    return [get_album_by_node(node) for node in node_list]

def get_closest(node):
    distance = nx.single_source_dijkstra_path_length(G, node, weight='reverse_weight')
    return sorted(distance, key=distance.get)[1:]

def get_in_community(node):
    community_index = node_to_community[node]
    node_community = communities[community_index]
    node_community.remove(node)
    return node_community

def main():
    print(get_in_community(1))

if __name__ == "__main__":
    main()