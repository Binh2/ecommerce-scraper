REGEXES = {
  "shopee": {
    "product_regular_price": {
      "regex": "[₫\.]",
      "replace": ""
    },
    "product_sale_price": {
      "regex": "[₫\.]",
      "replace": ""
    },
    # "product_image_urls": {
    #   "regex_type": "search",
    #   "regex": r'(?:url\(")(.*)(?:"\))',
    # }
  }
}