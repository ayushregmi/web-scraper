import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://fbref.com"
# url = "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
# url = "https://fbref.com/en/comps/Big5/2021-2022/stats/players/2021-2022-Big-5-European-Leagues-Stats"
url_header = {'User-Agent': 'Custom'}

url_list = [
    "https://fbref.com/en/comps/Big5/2019-2020/stats/players/2019-2020-Big-5-European-Leagues-Stats",
    "https://fbref.com/en/comps/Big5/2020-2021/stats/players/2020-2021-Big-5-European-Leagues-Stats",
    "https://fbref.com/en/comps/Big5/2021-2022/stats/players/2021-2022-Big-5-European-Leagues-Stats",
    "https://fbref.com/en/comps/Big5/stats/players/Big-5-European-Leagues-Stats"
]

stats_url = []

for url in url_list:
    html = requests.get(url=url, headers=url_header).text
    soup = BeautifulSoup(html, "html.parser")

    soup = soup.find_all("ul")[3].find_all('li', recursive=False)[3].find_all("li")
    for l in soup:
        # print(l.find("a")['href'])
        stats_url.append(base_url+l.find("a")['href'])

def get_Data(url, url_header=None):
    html = requests.get(url=url, headers=url_header).text
    
    soup = BeautifulSoup(html, "html.parser")
    temp = soup.find("div", {"id": "content"})
    
    temp_len = len(temp.find_all("h2"))
    
    print(temp.find_all("h2")[temp_len-2].text)

    # csv_name = '_'.join(temp.find_all("h2")[1].text.split(' '))
    csv_name = '_'.join(temp.find_all("h2")[temp_len-2].text.split(' '))
    table_columns = []
    
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
    
    statsFrame.to_csv(csv_name+".csv", index=True)
    return statsFrame

for i, url in enumerate(stats_url):
    get_Data(url)
    # print(i)
