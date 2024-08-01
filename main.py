from soup import *


def main():
    page = get_page(url)
    get_all_info(url, param_url, page)


if __name__ == "__main__":
    main()
