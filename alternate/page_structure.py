import re

# classes for Alternate
GRID_PRODUCT = re.compile("card align-content-center productBox boxCounter campaign-timer-container")
TITLE = re.compile("product-name")
LINK_TO_PRODUCT = "href" # child of TITLE
SPECS = "product-info" # sibling of TITLE
PREVIOUS_PRICE = re.compile("campaign-timer-striked-price-section")
CURRENT_PRICE = 'price'