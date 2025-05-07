import re

# classes for Coolblue
GRID_PRODUCT = re.compile("card-item card-standard")
TITLE = "card-v2-title-wrapper"
LINK_TO_PRODUCT = "href" # child of TITLE
PREVIOUS_PRICE = 'pricing rrp-lp30d'
CURRENT_PRICE = 'product-new-price'