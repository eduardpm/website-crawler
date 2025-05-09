from bs4 import BeautifulSoup
from emag.config import EMAG_CRAWLER_CONFIG, EMAG_WEBPAGE_CONFIG
from common.crawler.crawler_model import AbstractCrawler, CrawlerConfig, WebpageConfig
from common.products.product_models import Product, get_product_type_to_class_map
from common.products.product_types import ProductTypes


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


class EmagCrawler(AbstractCrawler):
    """
    Crawler for Emag website.
    """

    name: str = "emag"
    description: str = "Crawler for Emag website"
    crawler_configs: dict[ProductTypes, CrawlerConfig] = EMAG_CRAWLER_CONFIG
    webpage_config: WebpageConfig = EMAG_WEBPAGE_CONFIG
    found_products: list[Product] = []

    def parse(self, data: BeautifulSoup, product_type: ProductTypes) -> list[Product]:
        products = []
        for product in data.find_all(class_=self.webpage_config.grid_product):
            # if there is a previous price, it means it's a discount
            # if not, we can ignore the product
            if not (
                prev_price := product.find(class_=self.webpage_config.previous_price)
            ) or not prev_price.get_text(strip=True):
                continue

            products.append(
                get_product_type_to_class_map()[product_type](
                    title=product.find(class_=self.webpage_config.title).get_text(
                        strip=True
                    ),
                    link=product.find(class_=self.webpage_config.title)
                    .find("a")
                    .get("href"),
                    previous_price=get_price(
                        product.find(
                            class_=self.webpage_config.previous_price
                        ).get_text(strip=True)
                    ),
                    current_price=get_price(
                        product.find(class_=self.webpage_config.current_price).get_text(
                            strip=True
                        )
                    ),
                )
            )

        return products


EMAG_CRAWLER = EmagCrawler()
