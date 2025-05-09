from abc import abstractmethod
import re
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field
import requests

from common.products.product_models import Product
from common.products.product_types import ProductTypes
from common.utils.responses import Response


class CrawlerConfig(BaseModel):
    """
    Configuration class for crawlers.
    The configuration is for a single product type.
    """

    url_template: str = Field(..., description="URL template to crawl")
    max_pages: int = Field(..., description="Maximum number of pages to crawl")


class WebpageConfig(BaseModel):
    grid_product: str | re.Pattern
    title: str | re.Pattern
    link_to_product: str | re.Pattern
    specs: str | re.Pattern | None = None
    previous_price: str | re.Pattern
    current_price: str | re.Pattern


class AbstractCrawler(BaseModel):
    """
    Abstract base class for crawlers.
    """

    name: str = Field(..., description="Name of the crawler")
    description: str = Field(..., description="Description of the crawler")
    crawler_configs: dict[ProductTypes, CrawlerConfig] = Field(
        default_factory=dict,
        description="Crawler configurations for different product types",
    )
    webpage_config: WebpageConfig = Field(
        default_factory=WebpageConfig,
        description="Webpage configurations for parsing",
    )
    found_products: list[Product] = Field(
        default_factory=list, description="List of found products"
    )

    @staticmethod
    def get_urls(url_template: str, max_pages: int = 10) -> list[str]:
        return [url_template.format(page) for page in range(1, max_pages + 1)]

    @staticmethod
    def crawl(url: str) -> Response:
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

    def process_urls(
        self, urls: list[str], product_type: ProductTypes
    ) -> list[Product]:
        """
        Process the URLs and return a list of products.
        """
        aggregated_products = []
        for url in urls:
            print(f"Crawling {url}...")
            response = self.crawl(url)
            if response.status != 200:
                print(
                    f"Failed to crawl {url}. Status code: {response.status}. Reason: {response.message}"
                )
                break
            if response.data is None:
                print(f"No data found for {url}.")
                continue
            products = self.parse(response.data, product_type)
            if not products:
                print(f"No products found for {url}.")
                continue
            aggregated_products.extend(products)
        return aggregated_products

    def crawl_product(self, product_type: ProductTypes) -> None:
        """
        Crawl a specific product type and store the results in `found_products`.
        """
        if product_type not in self.crawler_configs:
            print(f"Product type {product_type} is not supported.")
            return

        config = self.crawler_configs[product_type]
        urls = self.get_urls(config.url_template, config.max_pages)

        products = self.process_urls(urls, product_type)
        if not products:
            print(f"No products found for {product_type}.")
            return

        self.found_products.extend(products)
        print(f"Found {len(products)} products for {product_type}.")
        for product in products:
            print(product)

    def crawl_all(self) -> None:
        """
        Crawl all product types defined in the crawler configurations.
        """
        for product_type in self.crawler_configs:
            self.crawl_product(product_type)

    @abstractmethod
    def parse(self, data: BeautifulSoup, product_type: ProductTypes) -> list[Product]:
        """
        Abstract method to be implemented by subclasses for parsing data.
        """
        pass
