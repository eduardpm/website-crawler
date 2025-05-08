from collections.abc import Callable
from bs4 import BeautifulSoup
import requests

from libs.models.products import Product
from libs.models.responses import Response


def crawl_website(url: str) -> Response:
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/124.0.0.0 Safari/537.36"
        ),
        "Accept-Language": "en-US,en;q=0.9",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Referer": "https://www.google.com",
    }
    # Send a GET request to the website
    response = requests.get(url, headers=headers)

    soup = None

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the HTML content using BeautifulSoup``
        soup = BeautifulSoup(response.content, "html.parser")

    return Response(
        status=response.status_code,
        message=response.reason,
        data=soup,
    )


def process_urls(urls: list[str], parser: Callable) -> list[Product]:
    aggregated_products = []
    for url in urls:
        print(f"Crawling {url}...")
        response = crawl_website(url)
        if response.status != 200:
            print(
                f"Failed to crawl {url}. Status code: {response.status}. Reason: {response.message}"
            )
            break
        if response.data is None:
            print(f"No data found for {url}.")
            continue
        products = parser(response.data)
        if not products:
            print(f"No products found for {url}.")
            continue
        aggregated_products.extend(products)
    return products
