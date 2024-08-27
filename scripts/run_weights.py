import os
import ast
import graph_generator

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)

with open(os.path.join(root_dir, './/data//test_weights.txt'), 'r') as f:
    lines = f.readlines()
    for i, line in enumerate(lines):
        weights = {}
        weights = ast.literal_eval(line)
        out_dir = os.path.join(root_dir, 'data', 'drafts', 'graphs', f'graph{i+1}')
        os.makedirs(out_dir, exist_ok=True)
        graph_generator.generate_graph(weights, out_dir)