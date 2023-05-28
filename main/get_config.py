import argparse
import constants


def get_config():
  argParser = argparse.ArgumentParser(description="Arguments to feed into browser driver")
  # argParser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, 
  #   help='Show this help message and exit.')
  argParser.add_argument("-w", "--website", default="amazon", help="Website could be shopee/amazon/lazada")
  argParser.add_argument("-k", "--keyword", default="vacuum robot", help="Keyword for the ecommerce search page")
  argParser.add_argument("-n", "--number-of-products", type=int, default=200, help="The upperbound for the number of products to get")
  argParser.add_argument("-d", "--delay", default=10, help="The delay (in second) to wait for each element to load")
  argParser.add_argument("-a", "--api-key", default=constants.CURRENCY_CONVERTER_API_KEY, help="API key to use currency converter API. Get yours for free from https://api.apilayer.com")
  argParser.add_argument("-p", "--post-automatically", action='store_true', help="Automatically post product to website after fetched all products")
  argParser.add_argument("-s", "--skip-scraping", action="store_true", help="For debugging purposes, skip the scraping code and import product.csv instead")
  argParser.add_argument("-l", "--left", default=0, type=int, help="For debugging purposes, get products in the range of [l, r)")
  argParser.add_argument("-r", "--right", default=None, type=int, help="For debugging purposes, get products in the range of [l, r)")
  args = argParser.parse_args()
  config = vars(args)
  return config