import re
from common.crawler.crawler_model import CrawlerConfig, WebpageConfig
from common.products.product_types import ProductTypes

MAX_PAGES = 10
EMAG_CRAWLER_CONFIG: dict[ProductTypes, CrawlerConfig] = {
    ProductTypes.RAM: CrawlerConfig(
        url_template="https://www.emag.ro/memorii/p{}/c",
        max_pages=MAX_PAGES,
    ),
    ProductTypes.VIDEO_CARD: CrawlerConfig(
        url_template="https://www.emag.ro/placi_video/p{}/c",
        max_pages=MAX_PAGES,
    ),
}

EMAG_WEBPAGE_CONFIG: WebpageConfig = WebpageConfig(
    grid_product=re.compile("card-item card-standard"),
    title="card-v2-title-wrapper",
    link_to_product="href",
    previous_price="pricing rrp-lp30d",
    current_price="product-new-price",
)
