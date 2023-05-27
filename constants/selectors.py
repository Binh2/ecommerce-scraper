from collections import OrderedDict
import math
from selenium.webdriver.common.by import By
import re
from validate_url import validate_url
from currency_converter import CurrencyConvertor
import functions


usd_to_vnd = CurrencyConvertor()
SELECTORS = {
  "shopee": {
    "product": { # special (doesn't process the normal way)
      "selector": ".shopee-search-item-result__item a",
      "attribute": "href",
    },
    "product_next_page": ".shopee-icon-button.shopee-icon-button--right",
    "product_image_urls": {
      "is_multiple_elements": True,
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
    "product_rating_amount": "._1k47d8:not(._046PXf)",
    "product_description": {
      "selector_type": By.CSS_SELECTOR,
      "selector": ".f7AU53",
      "attribute": "innerHTML",
    },
    # "product_tags": "",
    # "product_categories": "",
    "product_stock_number": "._6lioXX .flex div:nth-child(2)",
  }, 
  
  "amazon": OrderedDict({
    "product": {
      "selector": ".rush-component h2 a",
      "attribute": "href",
    },
    "product_next_page": ".s-pagination-next",
    "product_thumpnail_image_urls": {
      "is_multiple_elements": True,
      "selector": ".item.imageThumbnail",
      "action": "click",
      "concatenate_function": lambda texts: ",".join([ functions.encode_url(text) for text in texts if validate_url(text)]),
    },
    
    # Need to hover over all the thumpnails first because image is lazy loaded
    "product_image_urls": {
      "is_multiple_elements": True,
      "selector": ".imgTagWrapper img",
      "attribute": "src",
      "concatenate_function": lambda texts: ",".join([ functions.encode_url(text) for text in texts if validate_url(text)]),
    },
    "product_title": "h1 #productTitle",
    "product_regular_price": {
      "selector": "#corePriceDisplay_desktop_feature_div .a-price.a-text-price span:not(.a-offscreen)",
      "transform_function": lambda text: str(math.ceil(usd_to_vnd(float(text))))
    },
    "product_sale_price": {
      "is_multiple_elements": True,
      "selector": '#corePrice_feature_div .a-price span[aria-hidden="true"]',
      "transform_function": lambda text: str(math.ceil(usd_to_vnd(float(text)))),
      "concatenate_function": lambda texts: next((text for text in texts if text != ""), None),
    },
    "product_rating": {
      "selector": "#averageCustomerReviews #acrPopover",
      "attribute": "title",
    },
    "product_rating_amount": '#averageCustomerReviews #acrCustomerReviewText',
    "product_description": {
      "selector": "#featurebullets_feature_div ul",
      "attribute": "innerHTML",
    },
    "product_brand": {
      "selector_type": By.XPATH,
      "selector": "//div[@id='productOverview_feature_div']//text()[.='Brand']//ancestor::tr/td[position()=2]"
    },
    # "product_tags": "",
    # "product_categories": "",
    # "product_stock_number": "._6lioXX .flex div:nth-child(2)",
  }),
  "lazada": OrderedDict({
    "product": {
      "selector": ".RfADt a",
      "attribute": "href",
    },
    "product_next_page": ".ant-pagination-next .ant-pagination-item-link",

    # This will be handle by a special function. product_image_urls will use this element's concatenate_function
    "product_thumpnail_image_urls": {
      "is_multiple_elements": True,
      "selector": ".item-gallery__thumbnail-image",
      "action": "hover",
      "concatenate_function": lambda texts: ",".join([ functions.encode_url(text) for text in texts if validate_url(text)]),
    },
    
    # Need to hover over all the thumpnails first because image is lazy loaded
    "product_image_url": {
      "selector": ".gallery-preview-panel__image",
      "attribute": "src",
    },
    "product_title": ".pdp-mod-product-badge-title",
    "product_regular_price": ".pdp-price_size_xs",
    "product_sale_price": ".pdp-price_size_xl",
    # "product_rating": {
    #   "selector": "#averageCustomerReviews #acrPopover",
    #   "attribute": "title",
    # },
    "product_rating_amount": {
      "selector": '.pdp-review-summary__link',
    },
    "product_description": {
      "selector": ".pdp-product-desc",
      "attribute": "innerHTML",
      "action": "scroll,get"
    },
    "product_brand": ".pdp-product-brand__brand-link"
  }),
}