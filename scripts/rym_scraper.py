"""
This file scrapes chart data from local RateYourMusic html files
"""

import os
import csv
from bs4 import BeautifulSoup

PAGE_NUM = 25
pos = 1
script_dir = os.path.dirname(__file__)
with open("rym_list.csv", "w", newline='', encoding="utf-8") as csvfile:
    fieldnames = ['pos', 'artist', 'album', 'year', 'genre', 'second_genre',
                                     'descriptor', 'average', 'ratings']
    listwriter = csv.writer(csvfile)

    listwriter.writerow(fieldnames)
    for i in range(1, PAGE_NUM+1):
        filepath = os.path.join(script_dir, f"RYM_Pages\\{i}.html")
        with open(filepath, "r", encoding="utf-8") as page:
            html = page.read()
            S = BeautifulSoup(html, 'lxml').find('div', {"id": "content_wrapper_outer"}).find('div',
                            {"id": "content_wrapper"}).find('div', {"id": "content"})
            chart = S.find('sections').find('section', {"id": "page_charts_section_charts"})
            while pos <= i*40:
                entry = chart.find('div', {"id": f"pos{pos}"}).find('div',
                                {"class": "page_charts_section_charts_item_info"})
                top_line = entry.find('div', {"class": "page_charts_section_charts_top_line"})
                top_line_title = top_line.find(
                           'div', {"class": "page_charts_section_charts_top_line_title_artist"})
                album = top_line_title.find('div', {"class":
                        "page_charts_section_charts_item_title"}).a.span.span.text                
                artist = []
                artist_div = top_line_title.find('div', {"class":
                        "page_charts_section_charts_item_credited_links_primary"})
                if artist_div.a is None:
                    artist = ["Various"]
                else:
                    artist_span = [e.span for e in artist_div.find_all('a') if e.span is not None]
                    for span in artist_span:
                        if span.span is None:
                            artist.append("!")
                            artist.append(f"{span.text.lstrip()}")
                        else:
                            artist.append(span.span.text.lstrip())
                date = entry.find('div',{"class": "page_charts_section_charts_item_date"}).span.text
                year = date[-4:]
                genre_div = entry.find('div',
                            {"class": "page_charts_section_charts_item_genres_primary"})
                genre = [e.text for e in genre_div.find_all('a') if e.text is not None]
                second_div = entry.find('div',
                            {"class": "page_charts_section_charts_item_genres_secondary"})
                if second_div is None:
                    second_genre = [""]
                else:
                    second_genre = [e.text for e in second_div.find_all('a') if e.text is not None]
                descriptor_div = entry.find('div',
                                 {"class": "page_charts_section_charts_item_genre_descriptors"})
                descriptor = [e.text for e in descriptor_div.find_all('span') if e.text is not None]
                stats_div = top_line.find('div', {"class": "page_charts_section_charts_item_stats"})
                average = stats_div.find('span',
                          {"class": "page_charts_section_charts_item_details_average_num"}).text
                ratings = stats_div.find('span', {"class":
                                         "page_charts_section_charts_item_details_ratings"}).find(
                                         'span', {"class": "full"}).text.strip().replace(",", "")
                #print(f"{pos} - {artist}: {album} ({average} - {ratings})")
                listwriter.writerow([pos, artist, album, year, genre, second_genre,
                                     descriptor, average, ratings])
                pos += 1
