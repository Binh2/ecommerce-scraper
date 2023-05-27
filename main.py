import sys
import constants
import constant_interpreters
import csv
from currency_converter import CurrencyConvertor
import argparse
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from pprint import pprint
import selenium_extended_expected_conditions as EEC
from selectors_processor import SelectorsProcessor
import functions



def get_config():
  argParser = argparse.ArgumentParser(description="Arguments to feed into browser driver")
  # argParser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, 
  #   help='Show this help message and exit.')
  argParser.add_argument("-w", "--website", default="amazon", help="Website could be shopee or amazon")
  argParser.add_argument("-k", "--keyword", default="vacuum robot", help="Keyword for the ecommerce search page")
  argParser.add_argument("-n", "--number-of-products", default=200, help="The upperbound for the number of products to get")
  argParser.add_argument("-d", "--delay", default=10, help="The delay (in second) to wait for each element to load")
  argParser.add_argument("-a", "--api-key", default=constants.CURRENCY_CONVERTER_API_KEY, help="API key to use fixer API. Get yours for free from https://api.apilayer.com")
  argParser.add_argument("-l", "--left", default=0, type=int, help="For debugging purposes, get products in the range of [l, r)")
  argParser.add_argument("-r", "--right", default=None, type=int, help="For debugging purposes, get products in the range of [l, r)")
  args = argParser.parse_args()
  config = vars(args)
  return config

def init_driver(config: dict):
  URLS = constant_interpreters.UrlsConstant(config["website"])

  chrome_options = Options()
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--log-level=3')
  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.get(URLS["search"] + config["keyword"])
  driver.maximize_window()
  return driver

def write_to_csv(results):
  '''Write to CSV file'''
  ignored_element_names = ["product_rating", "product_rating_amount"]
  with open("products.csv", "w", encoding="utf_8", newline="") as csvFile:
    # csvFile.write("sep=@\n") # Uncomment this if you want to view it in excel (but can't import into wordpress)
    field_names = [ field_name for field_name in list(constants.element_name_to_field_name.values()) ]
    csvWriter = csv.DictWriter(csvFile, fieldnames=field_names, delimiter="@")
    csvWriter.writeheader()

    for result in results:
      row = { 
        constants.element_name_to_field_name[element_name]: result[element_name] 
        for element_name in result 
        if not element_name in ignored_element_names
      }
      pprint(row)
      csvWriter.writerow({ 
        constants.element_name_to_field_name[element_name]: result[element_name] 
        for element_name in result 
        if not element_name in ignored_element_names
      })

def main(driver: WebDriver, config: dict):
  delay = config["delay"]

  # Currency convertor should be call before SelectorsConstant
  usd_to_vnd = CurrencyConvertor(config["api_key"])

  SELECTORS = constant_interpreters.SelectorsConstant(config["website"])
  EXTENDED_SELECTORS = constant_interpreters.SelectorsConstant(config["website"], additional_info=True)
  URLS = constant_interpreters.UrlsConstant(config["website"])
  # REGEXES = constant_interpreters.RegexesConstant(config["website"])
  # EXTENDED_REGEXES = constant_interpreters.RegexesConstant(config["website"], additional_info=True)

  # Get all the product urls
  product_urls = []
  try:
    while len(product_urls) < int(config["number_of_products"]):
      WebDriverWait(driver, delay).until(EC.presence_of_element_located(SELECTORS["product"]))
      product_elements = iter(driver.find_elements(*SELECTORS["product"]))
      selector_info = EXTENDED_SELECTORS["product"][2]
      while len(product_urls) < int(config["number_of_products"]):
        try:
          product_element = next(product_elements)
        except StopIteration:
          break
        
        if selector_info["attribute"] == "":
          product_urls.append(product_element.text)
        else:
          product_urls.append(product_element.get_attribute(selector_info["attribute"]))

      next_page_button = WebDriverWait(driver, delay).until(EC.presence_of_element_located(SELECTORS["product_next_page"]))      
      next_page_button.click()

  except TimeoutException:
    print("Products page is not opening")
  assert(product_urls != [])
  print(f'{product_urls=}')

  # Init processor before get product info
  selectorsProcessor = SelectorsProcessor(driver, config["website"], delay)

  # Get product info
  results = []
  for product_url in product_urls[config["left"]:config["right"]]:
    print(product_url)
    driver.get(product_url)  
    driver.implicitly_wait(5)
    result = {}
    for element_name in SELECTORS:
      try:
        text = selectorsProcessor(element_name)
        if text == None:
          continue
        result[element_name] = text

      except:
        print(element_name)
        functions.handle_exception()
      
    results.append(result)
  return results

results = None
driver = None
try:
  config = get_config()
  driver = init_driver(config)
  results = main(driver, config)

  # Add brand at the start of description
  for i in range(len(results)):
    result = results[i]
    results[i]["product_description"] = f'<b>Thương hiệu: {result.get("product_brand", "")}</b>' + result.get("product_description", "")
  # print(results)
  
except:
  functions.handle_exception()

finally:
  try:
    write_to_csv(results)
  except:
    functions.handle_exception()

  driver.minimize_window()
  input("\n\n\nEnter to quit\n\n\n")
  driver.quit()