from pprint import pprint
import constant_processors


website = "amazon"
SELECTORS = constant_processors.SelectorsConstant(website)
pprint(SELECTORS["product_image_url"])