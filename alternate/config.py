import re
from common.crawler.crawler_model import CrawlerConfig, WebpageConfig
from common.products.product_types import ProductTypes

MAX_PAGES = 10
ALTERNATE_CRAWLER_CONFIG: dict[ProductTypes, CrawlerConfig] = {
    ProductTypes.RAM: CrawlerConfig(
        url_template="https://www.alternate.be/Geheugen?page={}",
        max_pages=MAX_PAGES,
    ),
    ProductTypes.VIDEO_CARD: CrawlerConfig(
        url_template="https://www.alternate.be/Grafische-kaarten?page={}",
        max_pages=MAX_PAGES,
    ),
}

ALTERNATE_WEBPAGE_CONFIG: WebpageConfig = WebpageConfig(
    grid_product=re.compile(
        "card align-content-center productBox boxCounter campaign-timer-container"
    ),
    title=re.compile("product-name"),
    link_to_product="href",
    specs="product-info",
    previous_price=re.compile("campaign-timer-striked-price-section"),
    current_price="price",
)
