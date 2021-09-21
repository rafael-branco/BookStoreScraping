import requests
from bs4 import BeautifulSoup

main_url = "https://books.toscrape.com/"


for i in range(1, 2):
    re = requests.get(main_url + "catalogue/page-" + str(i) + ".html")
    soup = BeautifulSoup(re.text, "html.parser")
    books = soup.select("section ol li div.image_container a")
    for item in books:
        print(item['href'])