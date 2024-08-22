"""
Read and analyze data from rym_list.csv 
"""

import os
import pandas as pd

ROOT_DIR = os.path.join(os.path.dirname(__file__), os.pardir)

def make_array(text):
    text = str(text)
    text = text.strip("[]")
    resulting_array = text.split(", ")
    for i in range(len(resulting_array)):
        resulting_array[i] = resulting_array[i].strip("'")
    return resulting_array

def get_count(df, data_type):
    df_list = []
    for line in df:
        line = make_array(line)
        for element in line:
            df_list.append(element)

    data = {
        f"{data_type}": df_list
    }

    new_df = pd.DataFrame(data)
    count = pd.crosstab(new_df[f"{data_type}"], "appearances")
    return count

def get_decade_count(df, data_type):

    def get_decade(year):
        return (int(year)//10)*10
    
    df_list = []
    for line in df:
        line = make_array(line)
        for element in line:
            decade = get_decade(element)
            df_list.append(decade)

    data = {
        f"{data_type}": df_list
    }

    new_df = pd.DataFrame(data)
    count = pd.crosstab(new_df[f"{data_type}"], "appearances")
    return count

def sort_count(count_file):
    count_sorted = count_file.sort_values(by='appearances', ascending=False)
    return count_sorted

def sorted_csv(df, col):
    sorted = df.sort_values(by=col)
    sorted.to_csv(ROOT_DIR + f'\data\graph\sorted_metrics\sorted_{col}')

filepath = os.path.join(ROOT_DIR, 'data', 'rym_list.csv')
data = pd.read_csv(filepath)

genre_count = sort_count(get_count(data["genre"], "genre"))
genre_count.to_csv(ROOT_DIR + '\data/counts/genre_count.csv')

second_genre_count = sort_count(get_count(data["second_genre"], "genre"))
second_genre_count.to_csv(ROOT_DIR + '\data/counts/second_genre_count.csv')

descriptor_count = sort_count(get_count(data["descriptor"], "descriptor"))
descriptor_count.to_csv(ROOT_DIR + '\data/counts/descriptor_count.csv')

decade_count = sort_count(get_decade_count(data["year"], "year"))
decade_count.to_csv(ROOT_DIR + '\data/counts/decade_count.csv')

graph_metrics = pd.read_csv(os.path.join(ROOT_DIR, 'data', 'graph', 'metrics.csv'))
for col in graph_metrics:
    sorted_csv(graph_metrics, col)