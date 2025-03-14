import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from bot import all_media_dir
from store_telega.crud import add_data, get_data


driver = webdriver.Chrome()


async def pars_file(filename: str):
    """
    Функция парсит конфигурационный файл и возвращает словарь с данными
    """
    # Выполняем чтение файла
    data = pd.read_excel(f"{all_media_dir}/{filename}")

    data_2 = []
    # Преобразуем полученные данные в словарь
    for i in data.to_dict(orient="records"):
        title = i["title"]
        url = i["url"]
        xpath = i["xpath"]
        driver.get(url)
        time.sleep(10)
        elem = driver.find_element(
            By.XPATH, xpath.split("/")[:-1] if xpath.endswith("/text()") else xpath
        )

        price = price_is_digit(str(elem.text))

        if price:
            data_2.append(
                {
                    "title": title,
                    "price": price,
                }
            )
        else:

            data_2.append(
                {
                    "title": title,
                    "price": "К сожалению на данном ресурсе не удалось найти нужную информацию",
                }
            )
        add_data(title=title, url=url, price=price)

    return data_2


async def get_average_price() -> dict:
    """
    Функция возвращает словарь с средними ценами по каждому сайту
    """
    data = get_data()
    average_prices = {}
    for item in data:
        if item["url"] in average_prices:
            average_prices[item["url"]][0] += 1
            average_prices[item["url"]][1] += float(
                item["price"] if item["price"] else 0,
            )
        else:
            average_prices[item["url"]] = [
                1,
                float(item["price"]) if item["price"] else 0,
            ]
    return average_prices


def price_is_digit(price: str) -> None | float:
    """
    Функция проверяет, является ли цена числом
    """
    new_price = ""
    for i in price.split():
        for j in i:
            if j.isdigit():
                new_price += j
    if new_price.isdigit():
        return float(new_price)
    return None
