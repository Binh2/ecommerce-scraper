from operator import itemgetter
import json
from woocommerce import API
import argparse

base_url = ''
consumer_key = ''
consumer_secret = ''

with open("ini.json") as file:
  obj = json.load(file)
  base_url, consumer_key, consumer_secret = itemgetter('base_url', 'consumer_key', 'consumer_secret')(obj)


parser = argparse.ArgumentParser(prog='WooCommerce API', description='CRUD products', epilog='Bye bye')
parser.add_argument('-a', '--action', choices=['c','r','u','d', ''], default='', nargs='?', help='To CRUD (Create/Read/Update/Delete) product')
parser.add_argument('-i', '--id', help='Only apply for RUD (Read/Update/Delete)')
args = parser.parse_args()
print(args)

# product = {
#   "name": "New product",
#   "type": "simple",
#   "regular_price": "19.99",
#   "description": "This is a new product",
#   "categories": "tai nghe",
# }

# wcapi = API(
#   url=base_url,
#   consumer_key=consumer_key,
#   consumer_secret=consumer_secret,
#   version="wc/v3",
#   timeout=10,
# )
# # res = wcapi.get("products")

# # print(res.status_code)
# # print(res.text)


# req = wcapi.post("products", json.dumps(product))
# print(req.json())