import requests
from bs4 import BeautifulSoup

main_url = "https://books.toscrape.com/"
id = 1

# DATABASE

'''
CREATE DATABASE IF NOT EXISTS book_store;
use book_store;
CREATE TABLE IF NOT EXISTS books (
	id INT PRIMARY KEY NOT NULL,
    title VARCHAR(300) NOT NULL,
    category VARCHAR(100) NOT NULL,
    price DOUBLE NOT NULL,
    stars int,
    prod_description LONGTEXT,
    upc VARCHAR(100),
    product_type VARCHAR(100),
    price_excl_tax DOUBLE,
    price_incl_tax DOUBLE,
    tax DOUBLE,
    availability INT NOT NULL,
    numb_reviews INT
);
'''

for i in range(1, 2):
    main_re = requests.get(main_url + "catalogue/page-" + str(i) + ".html")
    soup = BeautifulSoup(main_re.text, "html.parser")
    books = soup.select("section ol li div.image_container a")
    for item in books:
        re_book = requests.get(main_url + item['href'])
        soup = BeautifulSoup(re_book.text, "html.parser")
        title = soup.select_one("div.col-sm-6.product_main h1").text
        category = soup.select_one("ul.breadcrumb li:nth-child(2) a").text
        price = soup.select_one(".product_main p.price_color").text
        #stars
        prod_description = soup.select_one("div#product_description + p").text
        #upc = soup.select_one()

    main_re.close()