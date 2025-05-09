import re
from common.crawler.crawler_model import CrawlerConfig, WebpageConfig
from common.products.product_types import ProductTypes

MAIN_URL = "https://www.coolblue.be"
MAX_PAGES = 10
COOLBLUE_CRAWLER_CONFIG: dict[ProductTypes, CrawlerConfig] = {
    ProductTypes.RAM: CrawlerConfig(
        url_template="https://www.coolblue.be/en/ram/ram-for-desktops-with-windows-or-linux?page={}",
        max_pages=MAX_PAGES,
    ),
    ProductTypes.VIDEO_CARD: CrawlerConfig(
        url_template="https://www.coolblue.be/en/video-cards?page={}",
        max_pages=MAX_PAGES,
    ),
}

COOLBLUE_WEBPAGE_CONFIG: WebpageConfig = WebpageConfig(
    grid_product=re.compile("product-card grid"),
    title="product-card__title",
    link_to_product="href",
    specs="product-card__highlights",
    previous_price="sales-price__former",
    current_price="sales-price__current",
)
