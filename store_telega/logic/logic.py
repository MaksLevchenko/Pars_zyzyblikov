import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bot import all_media_dir
from store_telega.crud import add_data, get_data


options = Options()
options.add_argument("--headless")

driver = webdriver.Chrome(options=options)


def parse_page(url: str, xpath: str) -> tuple[str, float]:
    """
    Функция парсит страницу и возвращает цену товара
    """
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    element = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                xpath.split("/")[:-1] if xpath.endswith("/text()") else xpath,
            )
        )
    )
    price = price_is_digit(element.text)
    return price


async def pars_file(filename: str):
    """
    Функция парсит конфигурационный файл и возвращает словарь с данными
    """
    # Выполняем чтение файла
    data = pd.read_excel(f"{all_media_dir}/{filename}", engine="openpyxl")

    data_2 = []
    # Преобразуем полученные данные в словарь
    for i in data.to_dict(orient="records"):
        title = i["title"]
        url = i["url"]
        xpath = i["xpath"]

        price = parse_page(url, xpath)

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
    new_price = "".join([c for c in price if c.isdigit() or c == "." or c == ","])
    if new_price:
        return float(new_price)
    return None
