from emag.page_structure import CURRENT_PRICE, GRID_PRODUCT, PREVIOUS_PRICE, TITLE
from emag.urls import MAX_PAGES, RAMS, VIDEO_CARDS
from crawler import crawl_website

def get_price(price):
    """
    Get the price from the price string.
    """
    # price looks like this: 1.234,56 Lei
    # we need to remove the Lei and convert it to a float: remove the dot and replace the comma with a dot
    try:
        return float(price.split("Lei")[0].replace(".", "").replace(",", "."))
    except ValueError:
        return float(price.split("Lei")[0].replace("PRP:\xa0","").replace(".", "").replace(",", "."))

def parse_emag(soup):
    """
    Parse the soup object to extract product information from Coolblue.
    """
    products = []
    for product in soup.find_all(class_=GRID_PRODUCT):
        # if there is a previous price, it means it's a discount
        # if not, we can ignore the product
        if not (prev_price:=product.find(class_=PREVIOUS_PRICE)) or not prev_price.get_text(strip=True):
            continue
        title = product.find(class_=TITLE).get_text(strip=True)
        link = product.find(class_=TITLE).find('a').get("href")
        previous_price = get_price(product.find(class_=PREVIOUS_PRICE).get_text(strip=True))
        current_price = get_price(product.find(class_=CURRENT_PRICE).get_text(strip=True))

        products.append({
            'title': title,
            'link': link,
            'previous_price': previous_price,
            'current_price': current_price,
            'discount_percentage': round((previous_price - current_price) / previous_price * 100, 2)
        })
    print_emag(products)

def print_emag(products):
    """
    Print the product information in a readable format.
    """
    for product in products:
        print(f"Title: {product['title']}")
        print(f"Link: {product['link']}")
        print(f"Previous Price: {product['previous_price']}")
        print(f"Current Price: {product['current_price']}")
        print(f"Discount: {product['discount_percentage']}%")
        print("-" * 40)

def crawl_emag():
    def crawl_product(url):
        for page in range(1, MAX_PAGES + 1):
            url = url.format(page)
            if not crawl_website(url, parse_emag):
                print(f"Failed to crawl {url}. Next page likely not available.")
                break

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