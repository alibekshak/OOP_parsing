# How to sort something with key 
# def myFunc(e):
#   return len(e)

# cars = ['Ford', 'Mitsubishi', 'BMW', 'VW']

# cars.sort(reverse=True, key=myFunc)

# print(cars)

import requests
from bs4 import BeautifulSoup
from core.config import URL, HEADERS, DOMEN
import json


class Items():
    def __init__(self, url, header=HEADERS):
        self.url = url
        self.header = header

    def new_item(self):
        response = self.__response()
        soup = self.__soup(response)

        with open("core/index.html", "w") as file:
            file.write(str(soup))

        self._get_html()

    def __response(self):
        response = requests.get(url=self.url, headers=self.header)
        if response.status_code == 200:
            return response
        else:
            return f"Код ошибки {response.status_code}"

    def __soup(self, response):
        soup = BeautifulSoup(response.text, "lxml")
        all_div = soup.find("body")
        return all_div

    def _get_html(self):
        product = []
        with open("core/index.html", "r") as file:
            all_div = file.read()

        soup = BeautifulSoup(all_div, "lxml").find_all("form", method="post")

        for i in soup:
            try:
                product_url = DOMEN + i.find("div", class_="product_card-title").find("a").get("href")
                product_title = i.find("div", class_="product_card-title").find("a").text
                product_quantity = i.find("div", class_="card-quantity").text.strip()
                product_price = i.find("div", class_="product_card-prices").text.replace(" ", "")
            except Exception:
                continue
            else:
                all_items = {
                    "Название": product_title,
                    "Ссылка": product_url,
                    "Количество": product_quantity,
                    "Цена": product_price
                }

            product.append(all_items)

        with open(f"core/info.json", "w", encoding="UTF-8") as file:
            json.dump(product, file, indent=4, ensure_ascii=False)


parser = Items(url=URL)
parser.new_item()