import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://fbref.com"
url = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
url_header = {'User-Agent': 'Custom'}

html = requests.get(url=url, headers=url_header).text

soup = BeautifulSoup(html, "html.parser")

stats_url = []
soup = soup.find_all("ul")[3].find_all('li', recursive=False)[3].find_all("li")
for l in soup:
    stats_url.append(base_url+l.find("a")['href'])

def get_Data(url, url_header=None):

    table_columns = []
        
    html = requests.get(url=url, headers=url_header).text
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table")

    table_header = table.find("thead").find_all('tr')[1]
    for h in table_header.find_all("th")[1:]:
        table_columns.append(h.text.strip())

    statsFrame = pd.DataFrame(columns=table_columns)

    table_body = table.find("tbody")
    for row in table_body.find_all("tr"):
        try:
            if row['class']:
                continue
        except:
            temp = []
            cols = row.find_all("td")
            
            for col in cols:
                temp.append(col.text)
            statsFrame = pd.concat([statsFrame, pd.DataFrame([temp], columns=statsFrame.columns)], ignore_index=True)
                
    return statsFrame
    
    
initialFrame = get_Data(stats_url[0])

for url in stats_url[3:4]:
    initialFrame = initialFrame.merge(get_Data(url), on=["Player"], copy=False, how="outer", suffixes=("_DRIP", "_DROP"))
    
print(initialFrame)

print(initialFrame.columns)
print(initialFrame.iloc[0])