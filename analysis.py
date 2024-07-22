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

script_dir = os.path.dirname(__file__)
filepath = os.path.join(script_dir, "rym_list.csv")
data = pd.read_csv(filepath)

genre_count = get_count(data["genre"], "genre")
genre_count.to_csv('genre_count.csv')

second_genre_count = get_count(data["second_genre"], "genre")
second_genre_count.to_csv('second_genre_count.csv')
print(second_genre_count)

descriptor_count = get_count(data["descriptor"], "descriptor")
descriptor_count.to_csv('descriptor_count.csv')

decade_count = get_decade_count(data["year"], "year")
decade_count.to_csv('decade_count.csv')

