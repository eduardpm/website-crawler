from bs4 import BeautifulSoup
from emag.page_structure import CURRENT_PRICE, GRID_PRODUCT, PREVIOUS_PRICE, TITLE
from emag.urls import MAX_PAGES, RAMS, VIDEO_CARDS
from crawler import process_urls
from libs.models.products import Product


def get_price(price: str) -> float:
    """
    Get the price from the price string.
    """
    # price looks like this: 1.234,56 Lei
    # we need to remove the Lei and convert it to a float: remove the dot and replace the comma with a dot
    try:
        return float(price.split("Lei")[0].replace(".", "").replace(",", "."))
    except ValueError:
        return float(
            price.split("Lei")[0]
            .replace("PRP:\xa0", "")
            .replace(".", "")
            .replace(",", ".")
        )


def parse_emag(soup: BeautifulSoup) -> list[Product]:
    """
    Parse the soup object to extract product information from Coolblue.
    """
    products = []
    for product in soup.find_all(class_=GRID_PRODUCT):
        # if there is a previous price, it means it's a discount
        # if not, we can ignore the product
        if not (
            prev_price := product.find(class_=PREVIOUS_PRICE)
        ) or not prev_price.get_text(strip=True):
            continue

        products.append(
            Product(
                title=product.find(class_=TITLE).get_text(strip=True),
                link=product.find(class_=TITLE).find("a").get("href"),
                previous_price=get_price(
                    product.find(class_=PREVIOUS_PRICE).get_text(strip=True)
                ),
                current_price=get_price(
                    product.find(class_=CURRENT_PRICE).get_text(strip=True)
                ),
            )
        )
    return products


def crawl_emag() -> None:
    def crawl_product(url_template: str) -> None:
        urls = [url_template.format(page) for page in range(1, MAX_PAGES + 1)]
        products = process_urls(urls, parse_emag)

        for product in products:
            print(product)

    while True:
        print("Choose a product type to crawl:")
        print("1. Video Cards")
        print("2. RAM")
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
