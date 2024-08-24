import os
from analysis import make_array
import pandas as pd

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
filepath = os.path.join(root_dir, 'data', 'rym_list.csv')

data = open(filepath, "r", encoding='utf-8')
df = pd.read_csv(data)

"""
out format: dict parsedInfo = {item1: set(infos), item2: set(infos)}
"""

def get_info_by_node(nodeArray, infoArray):
    info = dict()
    for item in infoArray:
        item_info = []
        for line in df['pos']:
            if line in nodeArray:
                item_info.append(make_array(df[item][line-1]))
        parsedInfo = set()
        for i in item_info:
            for j in i:
                parsedInfo.add(j)
        info[item] = parsedInfo
    return info

def get_album_by_node(node):
    albums = []
    return df['album'][node-1]

def get_album_by_genre(genreArray):
    albums = []
    for index, line in enumerate(df['genre']):
        isInGenreArray = False
        parsedLine = make_array(line)
        for genre in parsedLine:
            if genre in genreArray:
                isInGenreArray = True
        if isInGenreArray:
            albums.append(df['album'][index])
    #adicionar funcao para buscar por genero secundario????
    return albums       

albums = get_album_by_genre(['Conscious Hip Hop', 'Jazz Rap'])
albums2 = get_info_by_node([1,2,3], ['genre', 'artist', 'album', 'year'])
