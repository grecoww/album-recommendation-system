import os
import networkx as nx
import pandas as pd
from graph_query import get_album_by_node

# Load graph and generate communities
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

# Transform node list into album list
def node_list_albums(node_list):
    return [get_album_by_node(node) for node in node_list]

# Generate list with closest albums
def get_closest(node):
    distance = nx.single_source_dijkstra_path_length(G, node, weight='reverse_weight')
    return sorted(distance, key=distance.get)[1:]

# Generate list with albums in the same community
def get_in_community(node):
    community_index = node_to_community[node]
    node_community = communities[community_index]
    node_community.remove(node)
    return node_community

def recommend(liked, disliked, recommended):
    pass # Return recommended node

def main():
    recommended = set() # Set that stores all listened albums, so there's no repetition
    liked = set()       # Set that stores all liked albums, used to get better recommendations 
    disliked = set()    # Set that stores all disliked albums, used to get better recommendations

    curr_node = int(input("Enter the position of the album you liked: "))
    recommended.add(curr_node)
    liked.add(curr_node)

    feedback = 1
    while True: # Input 0 to end
        # curr_node = recommend(liked, disliked, recommended)
        print(f"Your recommendation: {get_album_by_node(curr_node)}")
        recommended.add(curr_node)

        feedback = int(input("1: liked, 2: disliked, 0: exit\n"))
        if feedback == 1:
            liked.add(curr_node)
        elif feedback == 2:
            disliked.add(curr_node)

    print(get_in_community(1))

if __name__ == "__main__":
    main()