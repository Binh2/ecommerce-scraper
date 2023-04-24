from pprint import pprint
import constant_interpreters


website = "amazon"
SELECTORS = constant_interpreters.SelectorsConstant(website)
pprint(SELECTORS["product_image_url"])