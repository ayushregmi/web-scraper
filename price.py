import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.transfermarkt.us"
league_url = [
    "https://www.transfermarkt.us/premier-league/startseite/wettbewerb/GB1",
    "https://www.transfermarkt.us/la-liga/startseite/wettbewerb/ES1",
    "https://www.transfermarkt.us/serie-a/startseite/wettbewerb/IT1",
    "https://www.transfermarkt.us/bundesliga/startseite/wettbewerb/L1",
    "https://www.transfermarkt.us/ligue-1/startseite/wettbewerb/FR1"
]
url_header = {'User-Agent': 'Custom'}

club_url_list = []

players = pd.DataFrame(columns=['name', 'price'])

for url in league_url: 
    html = requests.get(url, headers=url_header).text

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all("table")[1].find("tbody")


    for row in table.find_all("tr"):
        club_url = row.find("a")
        club_url_list.append(base_url+club_url['href'])
    
players_list = []

for url in club_url_list:

    html = requests.get(url, headers=url_header).text

    soup = BeautifulSoup(html, "html.parser")

    table = soup.find_all("tbody")[1]
    

    for row in table.find_all("tr", recursive=False):
        col = row.find_all("td")
        
        price = col[len(col) - 1].text.strip()
        price = int(float(price[1:len(price)-1]) * (1000000 if price[len(price)- 1] == "m" else (1000 if price[len(price)- 1] == "k" else 0))) if price[1:len(price)-2] else None
        
        name = col[1].find_all("a")
        name = name[len(name)-1].text
        players_list.append({"name":name, "price":price})
        players = pd.concat([players, pd.DataFrame({"name":[name], "price":[price]})], ignore_index=True)


print(players)