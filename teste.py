import csv

with open('rym_list.csv', 'r', newline='', encoding='utf-8') as arquivo:
    reader = csv.reader(arquivo)

    for row in reader:
        artist = row[1]
        album = row[2]
    