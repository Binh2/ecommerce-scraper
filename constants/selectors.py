from selenium.webdriver.common.by import By
import re


SELECTORS = {
  "shopee": {
    "product": { # special (doesn't process the normal way)
      "selector": ".shopee-search-item-result__item a",
      "attribute": "href",
    },
    "product_next_page": "",
    "product_image_urls": {
      "multiple_elements": True,
      "selector": ".y4F\+fJ ._7eojrG div",
      "attribute": "style",
      "concatenate_function": lambda texts: ",".join([
        re.search(r'(?:url\(")(.*)(?:"\))', text).group(1) + ".jpeg" for text in texts
      ]),
    },
    "product_title": "._44qnta span",
    "product_regular_price": ".Y3DvsN",
    "product_sale_price": ".pqTWkA",
    "product_rating": "._1k47d8._046PXf",
    "product_rating_ammount": "._1k47d8:not(._046PXf)",
    "product_description": {
      "selector_type": By.CSS_SELECTOR,
      "selector": ".f7AU53",
      "attribute": "innerHTML",
    },
    # "product_tags": "",
    # "product_categories": "",
    "product_stock_number": "._6lioXX .flex div:nth-child(2)",
  }
}