from bs4 import BeautifulSoup
import requests
from bs4.element import Tag
import csv


url = "https://goldapple.ru/parfjumerija"
param_url = "?p="


def get_response(link):
    """
    Функция получения данных с html шаблона при успешном подлкючении
    :param link: обязательный параметр
    :return: возвращает часть шаблона html
    """
    response = requests.get(link)
    # проверка на успешное подключение
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "lxml")
        # получаем необходимую часть html для сбора данных
        main = soup.find("main")
        return main


def get_one_product(link: str):
    """
    Функция получает данные об одном продукте
    :param link: обязательный параметр
    :return: возвращает словать с данными одного продукта
    """
    main = get_response(link)
    description = main.find("div", {"itemprop": "description"})
    if description:
        description = description.get_text().replace("\n", "").replace("\xa0", "")
    manual = main.find("div", string="применение")
    manual = manual.get_text() if manual else "нет данных"
    country = "нет данных"
    country_info = main.find("div", {"value": "Text_4"})
    if country_info:
        country = country_info.find(string="страна происхождения")
        if country:
            country = country.find_next(string=True).strip()

    if country == "нет данных":
        brand_info = main.find("div", {"text": "о бренде"})
        country = brand_info.find("div").find_next().get_text().strip()

    if country == "нет данных":
        country_info = main.find("div", {"text": "Дополнительная информация"})
        if country_info:
            country = country_info.find(string="страна происхождения")
            if country:
                country = country.find_next(string=True).strip()

    return {
        "description": description,
        "manual": manual.replace("\n", ""),
        "country": country,
    }


def get_product(link: str, param: str, page: int):
    """
    Функция для сбора данных о продуктах со страницы
    :param param: обязательный параметр
    :param link: обязательный параметр
    :param page: обязательный параметр
    :return: словать со всеми данными о всех продуктах на странице
    """
    products_list = []
    main = get_response(f'{link}{param}{page}')
    main = main.select("div.IaefA > div.GyOMy > div")

    for item in main:
        for product in item:
            # проверка получаемого элемента на тип tag, для дальнейшей отработки
            if isinstance(product.find("a"), Tag):
                link = f"https://goldapple.ru{product.find('a').get('href')}"
                rating = product.find("a").find("div", class_="q7-dS")
                price = (
                    product.find("a").find("div", class_="DeuLT").get_text().strip()
                )
                name = (
                    f"{product.find('a').find(class_='BCQ9K').get_text()}"
                    f"{product.find('a').find(class_='SfclT').get_text()}"
                )
                if rating:
                    rating = rating.get_text().strip()
                else:
                    rating = "нет оценок"

                additional_info = get_one_product(link)

                if additional_info:
                    product_data = {
                        "link": link,
                        "name": name.replace("\xa0", ""),
                        "rating": rating,
                        "price": price,
                    }
                    # дополнение словаря о каждом продукте
                    product_data.update(additional_info)
                    products_list.append(product_data)
                    # запись данных в файл
                    with open(
                            "product.csv", "a", newline="", encoding="utf-8"
                    ) as file:
                        fieldnames = [
                            "link",
                            "name",
                            "rating",
                            "price",
                            "description",
                            "manual",
                            "country",
                        ]
                        writer = csv.DictWriter(file, fieldnames=fieldnames)

                        # Запись заголовка (имена ключей словаря)
                        writer.writeheader()
                        # Запись данных всех продуктов
                        for product_data in products_list:
                            writer.writerow(product_data)

    return products_list


def get_page(link: str):
    """
    Функция для получения последнее страницы с сайта
    :param link: обязательный параметр
    :return: номер последней страницы в формате числа
    """
    main = get_response(link)
    if main:
        # получение номера последней страницы
        pagination_links = main.find_all("span", {'aria-hidden': "true"})
        end_page = pagination_links[-1].get_text().strip()
        return int(end_page)


def get_all_info(link: str, param: str, page: int):
    """
    Функция для получения всех данных
    :param link: обязательный параметр
    :param param: обязательный параметр
    :param page: обязательный параметр
    :return: список со всеми данными о каждом продукте
    """
    products_list = []
    for i in range(1, page + 1):
        print(f"обратотано страниц {i}/{page}")
        products_list.append(get_product(f'{link}{param}{i}'))
    print('Закончен сбор данных и сохранен в файле "product.csv"')
    return products_list




