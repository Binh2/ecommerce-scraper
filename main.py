import time
import constants
import constant_processors
import csv
from handle_exception import handle_exception
from get_image import get_image
import argparse
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import re
import selenium_extended_expected_conditions as EEC


try:   
  argParser = argparse.ArgumentParser(description="Arguments to feed into browser driver")
  argParser.add_argument('-h', '--help', action='help', default=argparse.SUPPRESS, 
    help='Show this help message and exit.')
  argParser.add_argument("-w", "--website", default="shopee", help="Website could be shopee")
  argParser.add_argument("-k", "--keyword", default="tai nghe", help="Keyword for the ecommerce search page")
  argParser.add_argument("-n", "--number-of-products", default="1", help="The upperbound for the number of products to get")
  argParser.add_argument("-d", "--delay", default="60", help="The delay (in second) to wait for each element to load")
  args = argParser.parse_args()
  config = vars(args)
  delay = config["delay"]

  SELECTORS = constant_processors.SelectorsContant(config["website"])
  EXTENDED_SELECTORS = constant_processors.SelectorsContant(config["website"], additional_info=True)
  URLS = constant_processors.UrlsContant(config["website"])
  REGEXES = constant_processors.RegexesContant(config["website"])
  EXTENDED_REGEXES = constant_processors.RegexesContant(config["website"], additional_info=True)

  chrome_options = Options()
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--log-level=3')
  # driver = webdriver.Edge(EdgeChromiumDriverManager().install())
  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.get(URLS["search"] + config["keyword"])
  driver.maximize_window()
  # driver.implicitly_wait(5)

  # Get all the product urls
  product_urls = []
  try:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located(SELECTORS["product"]))
    product_elements = iter(driver.find_elements(*SELECTORS["product"]))
    selector_info = EXTENDED_SELECTORS["product"][2]
    while len(product_urls) < config["number_of_products"]:
      try:
        product_element = next(product_elements)
      except StopIteration:
        break
      
      if selector_info["attribute"] == "":
        product_urls.append(product_element.text)  
      else:
        product_urls.append(product_element.get_attribute(selector_info["attribute"]))

  except TimeoutException:
    print("Products page is not opening")
  assert(product_urls != [])

  results = []
  for product_url in product_urls:
    print(product_url)
    driver.get(product_url)  
    driver.implicitly_wait(5)
    result = {}
    for element_name in SELECTORS:
      try:
        if element_name == "product" or element_name == "product_next_page":
          continue

        else:
          WebDriverWait(driver, 60).until(EC.presence_of_element_located(SELECTORS[element_name]))
          selector_info = EXTENDED_SELECTORS[element_name][2]

          # Get text/attribute string from element(s)
          text = None
          if selector_info["multiple_elements"]:
            elements = driver.find_elements(*SELECTORS[element_name])
            texts = None
            if selector_info["attribute"] == "":
              texts = [ element.text for element in elements ]
            else:
              texts = [ element.get_attribute(selector_info["attribute"]) for element in elements ]
            text = selector_info["concatenate_function"](texts)
          else:
            element = driver.find_element(*SELECTORS[element_name])
            print(f'{EXTENDED_SELECTORS[element_name]=}')
            if selector_info["attribute"] == "":
              text = element.text
            else:
              text = element.get_attribute(selector_info["attribute"])
          assert(text != None)

          # Do regex (sub (subtitute) or search)
          processed_text = None
          regex_info = EXTENDED_REGEXES[element_name][2]
          # if regex_info["regex_type"] == "sub":
          processed_text = re.sub(*REGEXES[element_name], text)
          result[element_name] = processed_text

      except:
        handle_exception()
      
    results.append(result)

  print(results)

  # Write to CSV file
  with open("products.csv", "w", encoding="utf_8", newline="") as csvFile:
    # csvFile.write("sep=@\n") # Uncomment this if you want to view it in excel (but can't import into wordpress)
    field_names = [ field_name for field_name in list(constants.element_name_to_field_name.values()) ]
    csvWriter = csv.DictWriter(csvFile, fieldnames=field_names, delimiter="@")
    csvWriter.writeheader()

    for result in results:
      row = { 
        constants.element_name_to_field_name[element_name]: result[element_name] 
        for element_name in result 
        if element_name != "product_rating" and element_name != "product_rating_ammount" 
      }
      pprint(row)
      csvWriter.writerow({ 
        constants.element_name_to_field_name[element_name]: result[element_name] 
        for element_name in result 
        if element_name != "product_rating" and element_name != "product_rating_ammount" 
      })

except:
  handle_exception()
finally:
  driver.minimize_window()
  input("\n\n\nEnter to quit\n\n\n")
  driver.quit()