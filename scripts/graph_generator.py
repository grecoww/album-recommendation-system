"""
Script to calculate the edge weight based on the collected data
"""
import os
import pandas as pd
from analysis import make_array

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
filepath = os.path.join(root_dir+'\data', "rym_list.csv")
data = pd.read_csv(filepath)

# columns = {"artist": 5,"year": 3,"genre": 4,"second_genre": 2,"descriptor": 1}
# columns = {"artist": 5,"year": 3,"genre": 3,"second_genre": 0.8,"descriptor": 0.5}
columns = {"artist": 8,"year": 5,"genre": 3,"second_genre": 0.8,"descriptor": 0.3}


weights = []

for pos1 in range(1, 1001):
    for pos2 in range(pos1, 1001):
        if pos1 != pos2:
            weight = 0
            for column in columns:
                if column != "year":
                    album1 = make_array(data[column][pos1-1])
                    album2 = make_array(data[column][pos2-1])
                    for a1 in album1:
                        for a2 in album2:
                            if a1 == a2:
                                weight += columns[column]
                else:
                    if data[column][pos1-1]//10 == data[column][pos2-1]//10:
                        weight += columns[column]
                if (data["genre"][pos1-1] == data["second_genre"][pos2-1] or
                    data["genre"][pos2-1] == data["second_genre"][pos1-1]):
                    weight += columns["genre"]*columns["second_genre"]/2
            weights.append(round(weight, 1))
        else:
            weights.append(0)



node1 = []
node2 = []
for i in range(1,1001):
    for j in range(i,1001):
        node1.append(i)
        node2.append(j)

data = {
    'Node1': node1,
    'Node2': node2,
    'Weight': weights
}
graph_connections = pd.DataFrame(data)
graph_connections_filtered = graph_connections[graph_connections['Weight'] > 0]

max_weight = graph_connections_filtered.max(axis="rows")['Weight']
graph_connections_filtered['Reverse_Weight'] = round((max_weight + 1) - graph_connections_filtered['Weight'], 1)


graph_connections_filtered.to_csv(root_dir + '\data\graph\graph_connections.csv', index=False)