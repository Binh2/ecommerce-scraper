from operator import itemgetter
import json
from woocommerce import API


def init_wcapi():
  base_url = ''
  consumer_key = ''
  consumer_secret = ''

  with open("ini.json") as file:
    obj = json.load(file)
    base_url, consumer_key, consumer_secret = itemgetter('base_url', 'consumer_key', 'consumer_secret')(obj)

  wcapi = API(
    url=base_url,
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    version="wc/v3",
    timeout=10,
  )
  return wcapi

def get_products(id: int):
  wcapi = init_wcapi()
  res = wcapi.get("products")
  # print(res.status_code)
  # print(res.text)
  return res

def post_product(product: dict = {
    "name": "New product",
    "type": "simple",
    "regular_price": "19.99",
    "description": "This is a new product",
    "categories": "tai nghe",
  }):
  wcapi = init_wcapi()
  req = wcapi.post("products", json.dumps(product))
  # print(req.json())
  return req


if __name__ == "__main__":
  # res = post_product()
  # print(res.json())
  from pprint import pprint
  pprint(get_products(1844).text)
