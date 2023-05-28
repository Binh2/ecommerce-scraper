import json
import constants
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
from selectors_ import SelectorsProcessor
from urls import UrlsProcessor
import functions
import api
from main import *

def init_driver(config: dict):
  chrome_options = Options()
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--log-level=3')
  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.maximize_window()
  return driver

def rename_results_key(results, converter: dict = constants.element_name_to_api_field_name):
  return [
    {
      converter[element_name]: result[element_name] 
      for element_name in result
    } 
    for result in results
  ]

def post_to_website(results):
  '''Write to CSV file'''
  print(f'{results=}')
  ignored_element_names = ["product_rating", "product_rating_amount"]
  for result in results:
    res = api.post_product(result)
    print(f'{res.json()=}')

def main(driver: WebDriver, config: dict):
  delay = config["delay"]
  urlsProcessor = UrlsProcessor(driver, config["website"], config["keyword"], config["number_of_products"], delay)
  product_urls = urlsProcessor.run()

  # Init processor before get product info
  selectorsProcessor = SelectorsProcessor(driver, config["website"], delay)

  # Get product info
  results = []
  failed_product_url = []
  for product_url in product_urls[config["left"]:config["right"]]:
    print(product_url)
    driver.get(product_url)  
    driver.implicitly_wait(5)
    result = selectorsProcessor.run()
    if result == None:
      failed_product_url.append(product_url)
      continue
    print(f'{result=}')
    results.append(result)
  
  # with open('failed_product_urls.txt') as file:
  #   json.dump(failed_product_url, file)
  print(f'{failed_product_url=}')
  return results

if __name__ == "__main__":
  results = None
  driver = None
  try:
    config = get_config()
    results = None
    if config["skip_scraping"]:
      results = read_csv()

    else:
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
    print(results)
    try:
      if not config["skip_scraping"]:
        write_csv(results)
      
      if config["post_automatically"]:
        post_to_website(rename_results_key(results))
    except:
      functions.handle_exception()

    if driver:
      driver.minimize_window()
      input("\n\n\nEnter to quit\n\n\n")
      driver.quit()