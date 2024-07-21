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
    listwriter = csv.writer(csvfile)
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
                top_line = entry.find('div', {"class": "page_charts_section_charts_top_line"}).find(
                           'div', {"class": "page_charts_section_charts_top_line_title_artist"})
                album = top_line.find('div', {"class":
                        "page_charts_section_charts_item_title"}).a.span.span.text                
                artist_div = top_line.find('div', {"class":
                        "page_charts_section_charts_item_credited_links_primary"})
                if artist_div.a is None:
                    artist = "Various"
                else:
                    artist_span = artist_div.a.span
                    if artist_span.span is None: # TODO: more than one artist
                        artist = artist_span.text.lstrip()
                    else:
                        artist = artist_span.span.text.lstrip()
                date = entry.find('div',{"class": "page_charts_section_charts_item_date"}).span.text
                year = date[-4:]
                print(f"{pos} - {artist} - {album} ({year})")
                listwriter.writerow([pos, artist, album, year])
                pos += 1
