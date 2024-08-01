from soup import *


url_one = 'https://goldapple.ru/19000200199-blond-redhead-16-11'
url = "https://goldapple.ru/parfjumerija"
param_url = "?p="


def test_format_link(link):
    """
    Тест на проверку формата ссылки
    """
    try:
        assert isinstance(link, str), f'ссылка должна быть str'
        print(f'тест пройден: {link} верный формат ссылки')
    except AssertionError as e:
        print(f'Тест не пройден: {e}')


def test_get_response(link):
    """
    Тест на проверку успешного подключения и получения ответа от сервера.
    Проверяет, что возвращаемое значение является объектом типа bs4.element.Tag.
    """
    try:
        response = get_response(link)
        assert isinstance(response, Tag), f"Ожидаемый bs4.element.Tag, получен {type(response)}"
        print("Тест пройден: get_response вернул объект bs4.element.Tag.")
    except AssertionError as e:
        print(f"Тест не пройден: {e}")
    except Exception as e:
        print(f"Тест не пройден из-за непредвиденной ошибки:{e}")


def test_get_one_product(link):
    """
    Тест на проверку получаемых данных.
    Проверяет, что возвращаемое значение является объектом типа dict,
    данные являются объектом тип str и не равны None.
    """
    try:
        response = get_one_product(link)
        assert isinstance(response, dict), f"Ожидаемый объект dict, получен {type(response)}"
        print("Тест пройден: get_one_product вернул объект dict.")

        assert len(response) == 3, 'Ожидаемая длина должна быть равна 3'
        print('Тест пройдет: Ожидаемая длина равна 3')
        for item in response:
            assert isinstance(response[item], str), 'Ожидается объект класса str'
            print(f'Тест пройдет: получаемый объект "{item}" является str')

            assert response[item] is not None, f"Значение ключа '{item}' равно None"
            print(f'Тест пройдет: получаемый объект "{item}" не равен значению None')

    except AssertionError as e:
        print(f"Тест не пройден: {e}")
    except Exception as e:
        print(f"Тест не пройден из-за непредвиденной ошибки:{e}")


def test_get_product(func, link, param, page):
    """
    Тест на проверку получаемых данных.
    Проверяет, что возвращаемое значение является объектом типа list,
    данные являются объектом тип dict.
    """
    try:
        response = func(link, param, page)
        assert isinstance(response, list), f"Ожидается объект класса list, получен {type(response)}"
        print("Тест пройден: get_product вернул объект list.")

        assert len(response) >= 1, 'Ожидаемое количество элементов должно быть больше 1'
        print(f'Тест пройдет:Ожидаемое количество элементов больше 1. Получено элементов: {len(response)}.')
        for item in response:
            assert isinstance(item, dict), f'Ожидается объект класса dict, получен {type(item)}'
            print(f'Тест пройдет: получаемый объект является dict')
            assert len(item) == 7, 'Ожидаемое количество элементов должно быть равно 7'
            print(f'Тест пройдет:Полученное количество элементов равно 7')
    except AssertionError as e:
        print(f"Тест не пройден: {e}")
    except Exception as e:
        print(f"Тест не пройден из-за непредвиденной ошибки:{e}")


def test_get_page(link):
    """
    Тест на проверку получаемых данных.
    Проверяет, что возвращаемое значение является объектом типа int и не является None.
    """
    try:
        response = get_page(link)
        assert isinstance(response, int), f"Ожидается объект класса int, получен {type(response)}"
        print(f'Тест пройдет:Получен объект класса int')
        assert response is not None, 'Получен объект типа NoneType'
        print(f'Тест пройдет:Полученный объект не является None')

    except AssertionError as e:
        print(f"Тест не пройден: {e}")
    except Exception as e:
        print(f"Тест не пройден из-за непредвиденной ошибки:{e}")


if __name__ == "__main__":
    # Тесты для test_format_link
    print("Запуск тестов test_format_link...")
    test_format_link("https://example.com")
    test_format_link(123)
    test_format_link(None)

    # Тесты для test_get_response
    print("\nЗапуск тестов test_get_response...")
    test_get_response(url)
    test_get_response(None)

    # Тесты для test_get_one_product
    print("\nЗапуск тестов test_get_one_product...")
    test_get_one_product(url_one)
    test_get_one_product("https://invalid-url")

    # Тесты для test_get_product
    print("\nЗапуск тестов test_get_product...")
    test_get_product(get_product, url, param_url, 1)
    test_get_product(get_all_info, url, param_url, 1)
    test_get_product(get_product, "https://invalid-url", "?page=", 1)
    test_get_product(get_all_info, "https://invalid-url", "?page=", 1)

    # Тесты для test_get_page
    print("\nЗапуск тестов test_get_page...")
    test_get_page(url)
    test_get_page("https://invalid-url")
