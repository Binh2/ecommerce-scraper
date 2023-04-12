from selenium.webdriver.common.by import By


urls = {
  "shopee": {
    "base": "https://shopee.vn",
    "search": "https://shopee.vn/search?keyword=",
  }
}

selectors = {
  "shopee": {
    "product": ".shopee-search-item-result__item a",
    "product_image_urls": ".y4F\+fJ ._7eojrG div",
    "product_title": "._44qnta span",
    "product_regular_price": ".Y3DvsN",
    "product_sale_price": ".pqTWkA",
    "product_rating": "._1k47d8._046PXf",
    "product_rating_ammount": "._1k47d8:not(._046PXf)",
    "product_description": ".irIKAp",
    "product_stock_number": "._6lioXX .flex div:nth-child(2)",
  }
}

regex = {
  "shopee": {
    "product_regular_price": {
      "regex": "[₫\.]",
      "replace": ""
    },
    "product_sale_price": {
      "regex": "[₫\.]",
      "replace": ""
    },
  }
}

def get_selector(website: str, element: str):
  if isinstance(selectors[website][element], str):
    return (By.CSS_SELECTOR, selectors[website][element])
  return (selectors[website][element]["type"], selectors[website][element]["selector"])


element_name_to_field_name = {
  "": "ID",
  "product_type": "Type",
  "": "SKU",
  "product_title": "Name",
  "": "Published",
  "": "Is featured?",
  "": "Visibility in catalog",
  "": "Short description",
  "product_description": "Description",
  "": "Date sale price starts",
  "": "Date sale price ends",
  "": "Tax status",
  "": "Tax class",
  "": "In stock?",
  "product_stock_number": "Stock",
  "": "Low stock amount",
  "": "Backorders allowed?",
  "": "Sold individually?",
  "": "Weight(kg)",
  "": "Length(cm)",
  "": "Width(cm)",
  "": "Height(cm)",
  "": "Allow customer reviews?",
  "": "Purchase note",
  "product_sale_price": "Sale price",
  "product_regular_price": "Regular price",
  "": "Categories",
  "": "Tags",
  "": "Shipping class",
  "product_image_urls": "Images",
  "": "Download limit",
  "": "Download expiry days",
  "": "Parent",
  "": "Grouped products",
  "": "Upsells",
  "": "Cross-sells",
  "": "External URL",
  "": "Button text",
  "": "Position",
}