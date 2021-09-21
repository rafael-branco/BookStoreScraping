import requests
from bs4 import BeautifulSoup

main_url = "https://books.toscrape.com/"


for i in range(1, 2):
    main_re = requests.get(main_url + "catalogue/page-" + str(i) + ".html")
    soup = BeautifulSoup(main_re.text, "html.parser")
    books = soup.select("section ol li div.image_container a")
    for item in books:
        re_book = requests.get(main_url + item['href'])
        soup = BeautifulSoup(re_book.text, "html.parser")

    main_re.close()