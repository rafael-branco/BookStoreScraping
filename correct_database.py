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
            if (item_x == item_y[0]):
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
        # print(main_url + "catalogue/" + item['href'])
        soup = BeautifulSoup(re_book.text, "html.parser")

        category = soup.select_one("ul.breadcrumb li:nth-child(3) a").text
        sql = "UPDATE books SET category = %s WHERE id = %s"
        val = (category, id_counter)

        mycursor.execute(sql, val)
        mydb.commit()
        print(id_counter, "record inserted.")
        id_counter += 1
    main_re.close()

mydb.close()
