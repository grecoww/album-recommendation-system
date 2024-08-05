import os
import networkx as nx
import csv

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
filepath = os.path.join(root_dir+'\data\graph', "graph_connections.csv")

data = open(filepath, "r")
next(data, None)
Graphtype = nx.Graph()

G = nx.parse_edgelist(data, delimiter=',', create_using=Graphtype, nodetype=int, data=(('weight', float),))