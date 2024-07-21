"""
This file scrapes 
"""

import os

PAGE_NUM = 1
script_dir = os.path.dirname(__file__)

for i in range(1, PAGE_NUM+1):
    filepath = os.path.join(script_dir, f"RYM_Pages/{i}.html")
    with open(filepath, "r", encoding="utf-8") as page:
        html = page.read().decode("utf-8")
        print(html)
