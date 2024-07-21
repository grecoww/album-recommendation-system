"""
This file scrapes chart data from local RateYourMusic html files
"""

import os
from bs4 import BeautifulSoup

PAGE_NUM = 1
script_dir = os.path.dirname(__file__)

for i in range(1, PAGE_NUM+1):
    filepath = os.path.join(script_dir, f"RYM_Pages\\{i}.html")
    with open(filepath, "r", encoding="utf-8") as page:
        html = page.read()
        S = BeautifulSoup(html, 'lxml').find('div', {"id": "content_wrapper_outer"}).find('div',
                         {"id": "content_wrapper"}).find('div', {"id": "content"})
        chart = S.find('sections').find('section', {"id": "page_charts_section_charts"})
        for pos in range(1,41):
            entry = chart.find('div', {"id": f"pos{pos}"}).find('div',
                              {"class": "page_charts_section_charts_item_info"})
            print(entry)
