import requests
import bs4
from bs4 import BeautifulSoup
from decimal import Decimal
import re
import json
import mysql.connector

def getNumberOfStars(arr):
    list = [["One", 1], ["Two", 2], ["Three", 3], ["Four", 4], ["Five", 5]]
    for item_x in arr:
        for item_y in list:
            if(item_x == item_y[0]):
                return item_y[1]
    return 0

main_url = "https://books.toscrape.com/"

f = open('mysql.json', )
data = json.load(f)

mydb = mysql.connector.connect(
    host=data['mysql_info'][0]['host'],
    user=data['mysql_info'][0]['user'],
    password=data['mysql_info'][0]['password'],
    database=data['mysql_info'][0]['database']
)

mycursor = mydb.cursor()


id_counter = 1

for i in range(1, 51):
    main_re = requests.get(main_url + "catalogue/page-" + str(i) + ".html")
    soup = BeautifulSoup(main_re.text, "html.parser")
    books = soup.select("section ol li div.image_container a")
    for item in books:
        re_book = requests.get(main_url + "catalogue/" + item['href'])
        #print(main_url + "catalogue/" + item['href'])
        soup = BeautifulSoup(re_book.text, "html.parser")

        title = soup.select_one("div.col-sm-6.product_main h1").text
        category = soup.select_one("ul.breadcrumb li:nth-child(2) a").text
        price = soup.select_one(".product_main p.price_color").text
        price = Decimal(price[2:])
        stars = soup.select_one("p.star-rating")
        stars = getNumberOfStars(stars['class'])
        try:
            prod_description = soup.select_one("div#product_description + p").text
        except:
            prod_description = "None"
        upc = soup.select_one("#content_inner table.table.table-striped tr:nth-child(1) td").text
        product_type = soup.select_one("#content_inner table.table.table-striped tr:nth-child(2) td").text
        price_excl_tax = soup.select_one("#content_inner table.table.table-striped tr:nth-child(3) td").text
        price_excl_tax = Decimal(price_excl_tax[2:])
        price_incl_tax = soup.select_one("#content_inner table.table.table-striped tr:nth-child(4) td").text
        price_incl_tax = Decimal(price_incl_tax[2:])
        tax = soup.select_one("#content_inner table.table.table-striped tr:nth-child(5) td").text
        tax = Decimal(tax[2:])
        availability = soup.select_one("#content_inner table.table.table-striped tr:nth-child(6) td").text
        availability = int(re.search(r'\d+', availability).group())
        numb_reviews = int(soup.select_one("#content_inner table.table.table-striped tr:nth-child(7) td").text)

        sql = "INSERT INTO books (id, title, category, price, stars, prod_description, upc, product_type, price_excl_tax, price_incl_tax, tax, availability, numb_reviews) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
        val = (id_counter, title, category, price, stars, prod_description, upc, product_type, price_excl_tax, price_incl_tax, tax, availability, numb_reviews)
        mycursor.execute(sql, val)
        mydb.commit()
        print(mycursor.rowcount, "record inserted.")
        id_counter += 1
    main_re.close()

mydb.close()
