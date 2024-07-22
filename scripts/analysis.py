"""
Read and analyze data from rym_list.csv 
"""

import os
import pandas as pd

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

script_dir = os.getcwd()
filepath = os.path.join(script_dir+'\data', "rym_list.csv")
data = pd.read_csv(filepath)

genre_count = get_count(data["genre"], "genre")
genre_count_sorted = genre_count.sort_values(by='appearances', ascending=False)
genre_count_sorted.to_csv('data/counts/genre_count.csv')

second_genre_count = get_count(data["second_genre"], "genre")
second_genre_count_sorted = second_genre_count.sort_values(by='appearances', ascending=False)
second_genre_count_sorted.to_csv('data/counts/second_genre_count.csv')

descriptor_count = get_count(data["descriptor"], "descriptor")
descriptor_count_sorted = descriptor_count.sort_values(by='appearances', ascending=False)
descriptor_count_sorted.to_csv('data/counts/descriptor_count.csv')

decade_count = get_decade_count(data["year"], "year")
decade_count_sorted = decade_count.sort_values(by='appearances', ascending=False)
decade_count_sorted.to_csv('data/counts/decade_count.csv')

