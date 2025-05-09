from bs4 import BeautifulSoup
from alternate.config import ALTERNATE_CRAWLER_CONFIG, ALTERNATE_WEBPAGE_CONFIG
from common.crawler.crawler_model import AbstractCrawler, CrawlerConfig, WebpageConfig
from common.products.product_models import Product, get_product_type_to_class_map
from common.products.product_types import ProductTypes


class AlternateCrawler(AbstractCrawler):
    """
    Crawler for Alternate website.
    """

    name: str = "alternate"
    description: str = "Crawler for Alternate website"
    crawler_configs: dict[ProductTypes, CrawlerConfig] = ALTERNATE_CRAWLER_CONFIG
    webpage_config: WebpageConfig = ALTERNATE_WEBPAGE_CONFIG
    found_products: list[Product] = []

    def parse(self, data: BeautifulSoup, product_type: ProductTypes) -> list[Product]:
        products = []
        for product in data.find_all(class_=self.webpage_config.grid_product):
            # if there is a previous price, it means it's a discount
            # if not, we can ignore the product
            if not product.find(class_=self.webpage_config.previous_price):
                continue

            products.append(
                get_product_type_to_class_map()[product_type](
                    title=product.find(class_=self.webpage_config.title).get_text(
                        strip=True
                    ),
                    link=product.get("href"),
                    specs=product.find(class_=self.webpage_config.specs).get_text(
                        strip=True
                    ),
                    previous_price=float(
                        product.find(class_=self.webpage_config.previous_price)
                        .get_text(strip=True)
                        .split("€")[1]
                        .replace(".", "")
                        .replace(",", ".")
                        .strip()
                    ),
                    current_price=float(
                        product.find(class_=self.webpage_config.current_price)
                        .get_text(strip=True)
                        .split("€")[1]
                        .replace(".", "")
                        .replace(",", ".")
                        .strip()
                    ),
                )
            )

        return products


ALTERNATE_CRAWLER = AlternateCrawler()
