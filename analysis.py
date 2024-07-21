import os
import pandas as pd
import numpy as np

def makeArray(text):
    text = text.strip("[]")
    return np.fromstring(text, sep=', ')

script_dir = os.path.dirname(__file__)
filepath = os.path.join(script_dir, "rym_list.csv")
data = pd.read_csv(filepath)
df = data['genre']

print(makeArray("['hello', 'goodbye']"))
