from coolblue.page_structure import CURRENT_PRICE, GRID_PRODUCT, PREVIOUS_PRICE, SPECS, TITLE
from coolblue.urls import M_2_NVMES, MAIN_URL, MAX_PAGES, RAMS
from crawler import crawl_website

def parse_coolblue(soup):
    """
    Parse the soup object to extract product information from Coolblue.
    """
    products = []
    for product in soup.find_all(class_=GRID_PRODUCT):
        # if there is a previous price, it means it's a discount
        # if not, we can ignore the product
        if not product.find(class_=PREVIOUS_PRICE):
            continue
        title = product.find(class_=TITLE).get_text(strip=True)
        link = MAIN_URL + product.find(class_=TITLE).find('a').get("href")
        specs = product.find(class_=SPECS).get_text(strip=True)
        previous_price = int(product.find(class_=PREVIOUS_PRICE).get_text(strip=True).split(",")[0])
        current_price = int(product.find(class_=CURRENT_PRICE).get_text(strip=True).split(",")[0])

        products.append({
            'title': title,
            'link': link,
            'specs': specs,
            'previous_price': previous_price,
            'current_price': current_price,
            'discount_percentage': round((previous_price - current_price) / previous_price * 100, 2)
        })
    print_coolblue(products)

def print_coolblue(products):
    """
    Print the product information in a readable format.
    """
    for product in products:
        print(f"Title: {product['title']}")
        print(f"Link: {product['link']}")
        print(f"Specs: {product['specs']}")
        print(f"Previous Price: {product['previous_price']}")
        print(f"Current Price: {product['current_price']}")
        print(f"Discount: {product['discount_percentage']}%")
        print("-" * 40)

def crawl_coolblue():
    def crawl_product(url):
        for page in range(1, MAX_PAGES + 1):
            url = url.format(page)
            if not crawl_website(url, parse_coolblue):
                print(f"Failed to crawl {url}. Next page likely not available.")
                break

    while True:
        print("Choose a product type to crawl:")
        print("1. M.2 NVMe")
        print("2. RAM")
        print("3. Exit")

        choice = input("Enter your choice (1/2/3): ").strip()
        if choice == "1":
            crawl_product(M_2_NVMES)
            break
        elif choice == "2":
            crawl_product(RAMS)
            break
        elif choice == "3":
            print("Exiting the program.")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")