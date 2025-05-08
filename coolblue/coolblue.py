from bs4 import BeautifulSoup
from coolblue.page_structure import (
    CURRENT_PRICE,
    GRID_PRODUCT,
    PREVIOUS_PRICE,
    SPECS,
    TITLE,
)
from coolblue.urls import M_2_NVMES, MAIN_URL, MAX_PAGES, RAMS, VIDEO_CARDS
from crawler import process_urls
from libs.models.products import Product


def parse_coolblue(soup: BeautifulSoup) -> list[Product]:
    """
    Parse the soup object to extract product information from Coolblue.
    """
    products = []
    for product in soup.find_all(class_=GRID_PRODUCT):
        # if there is a previous price, it means it's a discount
        # if not, we can ignore the product
        if not product.find(class_=PREVIOUS_PRICE):
            continue

        products.append(
            Product(
                title=product.find(class_=TITLE).get_text(strip=True),
                link=MAIN_URL + product.find(class_=TITLE).find("a").get("href"),
                specs=product.find(class_=SPECS).get_text(strip=True),
                previous_price=int(
                    product.find(class_=PREVIOUS_PRICE)
                    .get_text(strip=True)
                    .split(",")[0]
                ),
                current_price=int(
                    product.find(class_=CURRENT_PRICE)
                    .get_text(strip=True)
                    .split(",")[0]
                ),
            )
        )
    return products


def crawl_coolblue():
    def crawl_product(url_template: str) -> None:
        urls = [url_template.format(page) for page in range(1, MAX_PAGES + 1)]
        products = process_urls(urls, parse_coolblue)

        for product in products:
            print(product)

    while True:
        print("Choose a product type to crawl:")
        print("1. M.2 NVMe")
        print("2. RAM")
        print("3. VIDEO CARDS")
        print("4. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            crawl_product(M_2_NVMES)
            break
        elif choice == "2":
            crawl_product(RAMS)
            break
        elif choice == "3":
            crawl_product(VIDEO_CARDS)
            break
        elif choice == "4":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
