import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://fbref.com"
url = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"

html = requests.get(url=url).text

soup = BeautifulSoup(html, "html.parser")

stats_url = []

soup = soup.find_all("ul")[3].find_all('li', recursive=False)[3].find_all("li")

for l in soup:
    stats_url.append(base_url+l.find("a")['href'])

url = stats_url[0]

table_columns = []
for url in stats_url:
    
    html = requests.get(url=url).text

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find("table")

    table_header = table.find("thead").find_all('tr')[1]


    for h in table_header.find_all("th"):
        h = h.text.strip()
    
        if h not in table_columns:
            table_columns.append(h)
    
print(table_columns)
