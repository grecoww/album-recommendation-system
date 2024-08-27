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
    node_community = communities[community_index].copy()
    node_community.remove(node)
    return node_community

def recommend(liked, disliked, recommended):
    general_list = []
    
    for album in liked:
        album_community_list = get_in_community(album)

        updated_general_list = []
        suggestion_list = get_closest(album)
        filtered_suggestion_list = enumerate(reversed([album for album in suggestion_list if album not in recommended]), start=1)
        for points1, album1 in filtered_suggestion_list:
            found = False
            for (points2, album2) in general_list:
                if album1==album2:
                    if album1 in album_community_list:
                        total_points = 1.5*(points1+points2)
                        updated_general_list.append((total_points, album1))
                        found = True
                        break
                    else:    
                        total_points = points1+points2
                        updated_general_list.append((total_points, album1))
                        found = True
                        break
            if not found:
                updated_general_list.append((points1, album1))

        general_list = updated_general_list

    for album in disliked:
        album_community_list = get_in_community(album)

        updated_general_list = []
        suggestion_list = get_closest(album)
        filtered_suggestion_list = enumerate(reversed([album for album in suggestion_list if album not in recommended]), start=1)
        for points1, album1 in filtered_suggestion_list:
            found = False
            for (points2, album2) in general_list:
                if album1==album2:
                    if album1 in album_community_list:
                        total_points = points2-(1.5*points1)
                        updated_general_list.append((total_points, album1))
                        break
                    else:
                        total_points = points2-points1
                        updated_general_list.append((total_points, album1))
                        break
        general_list = updated_general_list


    sorted_general_list = sorted(general_list, key=lambda x: x[0], reverse=True)
    suggested_album = sorted_general_list[0][1]
    return suggested_album
            



def main():
    recommended = set() # Set that stores all listened albums, so there's no repetition
    liked = set()       # Set that stores all liked albums, used to get better recommendations 
    disliked = set()    # Set that stores all disliked albums, used to get better recommendations

    curr_node = int(input("Enter the position of the album you liked: "))
    print(f"You liked the following album: {get_album_by_node(curr_node)}")
    recommended.add(curr_node)
    liked.add(curr_node)

    feedback = 1
    Running = 1
    while Running: # Input 0 to end
        curr_node = recommend(liked, disliked, recommended)
        recommended.add(curr_node)
        print(f"Your recommendation: {get_album_by_node(curr_node)}")

        try:
            feedback = int(input("1: liked, 2: disliked, 0: exit\n"))
            if feedback == 1:
                liked.add(curr_node)
                continue
            elif feedback == 2:
                disliked.add(curr_node)
                continue
            elif feedback == 0:
                Running = 0
            else:
                print('Enter a valid input!\n')
                continue
        except:
            print('Enter a valid input!\n')
            continue

if __name__ == "__main__":
    main()