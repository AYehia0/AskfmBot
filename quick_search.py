import requests
from bs4 import BeautifulSoup

headers = {
    "User-Agent": "Chrome/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.75 Safari/537.36"
}


search_key = input("Search me: ")
google_search_url = "https://www.google.com/search?hl=en&q="

r = requests.get(google_search_url+search_key, headers=headers).text

soup = BeautifulSoup(r, 'lxml')


inside_tag = "mh_tsuid47"
container_id = "iwp-tabs-container"

print(soup.find(class_="FLP8od"))
