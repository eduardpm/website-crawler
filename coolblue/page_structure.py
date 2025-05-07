import re

# classes for Coolblue
GRID_PRODUCT = re.compile("product-card grid")
TITLE = "product-card__title"
LINK_TO_PRODUCT = "href" # child of TITLE
SPECS = "product-card__highlights" # sibling of TITLE
PREVIOUS_PRICE = 'sales-price__former'
CURRENT_PRICE = 'sales-price__current'