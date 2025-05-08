from bs4 import BeautifulSoup
from alternate.page_structure import (
    CURRENT_PRICE,
    GRID_PRODUCT,
    PREVIOUS_PRICE,
    SPECS,
    TITLE,
)
from alternate.urls import MAX_PAGES, VIDEO_CARDS, RAMS
from crawler import process_urls
from libs.models.products import Product


def parse_alternate(soup: BeautifulSoup) -> list[Product]:
    """
    Parse the soup object to extract product information from Alternate.
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
                link=product.get("href"),
                specs=product.find(class_=SPECS).get_text(strip=True),
                previous_price=float(
                    product.find(class_=PREVIOUS_PRICE)
                    .get_text(strip=True)
                    .split("€")[1]
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                ),
                current_price=float(
                    product.find(class_=CURRENT_PRICE)
                    .get_text(strip=True)
                    .split("€")[1]
                    .replace(".", "")
                    .replace(",", ".")
                    .strip()
                ),
            )
        )

    return products


def crawl_alternate() -> None:
    def crawl_product(url_template: str) -> None:
        urls = [url_template.format(page) for page in range(1, MAX_PAGES + 1)]
        products = process_urls(urls, parse_alternate)

        for product in products:
            print(product)

    while True:
        print("Choose a product type to crawl:")
        print("1. VIDEO CARDS")
        print("2. RAMS")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            crawl_product(VIDEO_CARDS)
            break
        elif choice == "2":
            crawl_product(RAMS)
            break
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
