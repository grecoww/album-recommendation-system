import os
import pandas as pd
from analysis import make_array

"""
album1 = "6,['King Crimson'],In the Court of the Crimson King,1969,"['Progressive Rock', 'Art Rock']","['Symphonic Prog', 'Jazz-Rock', 'Free Improvisation', 'Psychedelic Rock']","['fantasy', 'epic', 'progressive', 'complex', 'poetic', 'philosophical', 'surreal', 'melancholic']",4.32,66924"
album2 = "27,['King Crimson'],Red,1974,"['Progressive Rock', 'Art Rock']","['Jazz-Rock', 'Hard Rock', 'Free Improvisation', 'Heavy Metal']","['dark', 'heavy', 'anxious', 'technical', 'uncommon time signatures', 'complex', 'ominous', 'progressive']",4.24,34700"
"""

root_dir = os.path.join(os.path.dirname(__file__), os.pardir)
filepath = os.path.join(root_dir+'\data', "rym_list.csv")
data = pd.read_csv(filepath)

columns = {"artist": 1,"year": 1,"genre": 1,"second_genre": 1,"descriptor": 1}

pos1 = 1
weights = []

for pos2 in range(1, 101):
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
                weight += columns["genre"]*columns["second_genre"]
        weights.append(weight)
    else:
        weights.append(0)
print(weights)