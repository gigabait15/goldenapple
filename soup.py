from bs4 import BeautifulSoup
import requests
from bs4.element import Tag
from pprint import pprint
import csv


def one_product(link):
    response = requests.get(link)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        main = soup.find('main')
        description = main.find('div', {'itemprop': "description"})
        if description:
            description = description.get_text().replace('\n', '').replace('\xa0', '')
        manual = main.find('div', string='применение')
        manual = manual.get_text() if manual else "нет данных"
        country = "нет данных"
        country_info = main.find('div', {'value': "Text_4"})
        if country_info:
            country = country_info.find(string='страна происхождения')
            if country:
                country = country.find_next(string=True).strip()

        if country == "нет данных":
            brand_info = main.find('div', {'text': 'о бренде'})
            country = brand_info.find('div').find_next().get_text().strip()

        if country == "нет данных":
            country_info = main.find('div', {'text': 'Дополнительная информация'})
            if country_info:
                country = country_info.find(string='страна происхождения')
                if country:
                    country = country.find_next(string=True).strip()

        return {
            'description': description,
            'manual': manual.replace('\n', ''),
            'country': country
        }

def get_product(page):
    link = f'https://goldapple.ru/parfjumerija?={page}'
    response = requests.get(link)
    products_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        main = soup.find('main').select('div.IaefA > div.GyOMy > div')
        for item in main:
            for product in item:
                if isinstance(product.find('a'), Tag):
                    link = f"https://goldapple.ru{product.find('a').get('href')}"
                    rating = product.find('a').find('div', class_='q7-dS')
                    price = product.find('a').find('div', class_="DeuLT").get_text().strip()
                    name = (f"{product.find('a').find(class_='BCQ9K').get_text()}"
                            f"{product.find('a').find(class_='SfclT').get_text()}")
                    if rating:
                        rating = rating.get_text().strip()
                    else:
                        rating = 'нет оценок'

                    additional_info = one_product(link)

                    if additional_info:
                        product_data = {
                            'link': link,
                            'name': name.replace('\xa0', ''),
                            'rating': rating,
                            'price': price
                        }
                        product_data.update(additional_info)
                        products_list.append(product_data)
                        with open('product.csv', 'a', newline='', encoding='utf-8') as file:
                            fieldnames = ['link', 'name', 'rating', 'price', 'description', 'manual', 'country']
                            writer = csv.DictWriter(file, fieldnames=fieldnames)

                            # Запись заголовка (имена ключей словаря)
                            writer.writeheader()

                            # Запись данных всех продуктов
                            for product_data in products_list:
                                writer.writerow(product_data)

        return products_list

def get_all_product():
    link = 'https://goldapple.ru/parfjumerija'
    response = requests.get(link)
    products_list = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'lxml')
        main = soup.find('main')
        pagination_links = main.find_all('a', class_='_9YPE6 E7TLT npgD5 PkQ1t')[-1]
        end_page = pagination_links.find('span', class_="K2EMr").get_text().strip()
        for i in range(1, int(end_page) + 1):
            print(f'обратотано страниц {i}/{end_page}')
            products_list.append(get_product(i))
    return products_list


if __name__ == "__main__":
    import datetime
    start = datetime.datetime.now()
    # # pprint(one_product("https://goldapple.ru/82812100001-cuir-celeste"))
    # # pprint(get_all_product())
    pprint(get_product(2))
    stop = datetime.datetime.now()
    print(stop - start)
