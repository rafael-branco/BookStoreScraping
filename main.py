import requests
import bs4
from bs4 import BeautifulSoup
from decimal import Decimal
import re


def getNumberOfStars(arr):
    list = [["One", 1], ["Two", 2], ["Three", 3], ["Four", 4], ["Five", 5]]
    for item_x in arr:
        for item_y in list:
            if(item_x == item_y[0]):
                return item_y[1]
    return 0

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
        re_book = requests.get(main_url + "catalogue/" + item['href'])
        print(main_url + "catalogue/" + item['href'])
        soup = BeautifulSoup(re_book.text, "html.parser")
        #print(soup)
        title = soup.select_one("div.col-sm-6.product_main h1").text
        category = soup.select_one("ul.breadcrumb li:nth-child(2) a").text
        price = soup.select_one(".product_main p.price_color").text
        price = Decimal(price[1:])
        stars = soup.select_one("p.star-rating")
        stars = getNumberOfStars(stars['class'])
        print(stars)
        prod_description = soup.select_one("div#product_description + p").text
        upc = soup.select_one("#content_inner table.table.table-striped tr:nth-child(1) td").text
        product_type = soup.select_one("#content_inner table.table.table-striped tr:nth-child(2) td").text
        price_excl_tax = soup.select_one("#content_inner table.table.table-striped tr:nth-child(3) td").text
        price_incl_tax = soup.select_one("#content_inner table.table.table-striped tr:nth-child(4) td").text
        tax = soup.select_one("#content_inner table.table.table-striped tr:nth-child(5) td").text
        availability = soup.select_one("#content_inner table.table.table-striped tr:nth-child(6) td").text
        availability = int(re.search(r'\d+', availability).group())
        numb_reviews = soup.select_one("#content_inner table.table.table-striped tr:nth-child(7) td").text

    main_re.close()
