import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

from bot import all_media_dir
from store_telega.crud import add_data


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
        time.sleep(5)
        elem = driver.find_element(
            By.XPATH, xpath.split("/")[:-1] if xpath.endswith("/text()") else xpath
        )

        data_2.append(
            {
                "title": title,
                "price": (
                    elem.text
                    if elem
                    else "К сожалению на данном ресурсе не удалось найти нужную информацию"
                ),
            }
        )
        add_data(title=title, url=url, price=elem.text)

    return data_2
