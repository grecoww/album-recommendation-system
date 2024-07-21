import sys

[page] = sys.argv[1:]
html = page.read().decode("utf-8")
print(html)