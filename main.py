import time
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
from constants import *
from selenium.webdriver.chrome.options import Options
from pprint import pprint
import re
import selenium_extended_expected_conditions as EEC


try:   
  argParser = argparse.ArgumentParser(description="Arguments to feed into browser driver")
  argParser.add_argument("-w", "--website", default="shopee", help="Website could be shopee")
  argParser.add_argument("-k", "--keyword", default="tai nghe", help="Keyword for the ecommerce search page")
  args = argParser.parse_args()
  config = vars(args)

  chrome_options = Options()
  # chrome_options.add_argument('--headless')
  chrome_options.add_argument('--log-level=3')
  # driver = webdriver.Edge(EdgeChromiumDriverManager().install())
  driver = webdriver.Chrome(ChromeDriverManager().install())
  driver.get(urls[config["website"]]["search"] + config["keyword"])
  driver.maximize_window()
  driver.implicitly_wait(5)
  product_urls = None
  try:
    WebDriverWait(driver, 60).until(EC.presence_of_element_located(get_selector(config["website"], "product")))
    product_elements = driver.find_elements(*get_selector(config["website"], "product"))[:1]
    product_urls = [ product_element.get_attribute("href") for product_element in product_elements]
  except TimeoutException:
    print("Products page is not opening")

  assert(product_urls != None)
  results = []
  for product_url in product_urls:
    print(product_url)
    driver.get(product_url)  
    driver.implicitly_wait(5)
    result = {}
    for element_name in selectors[config["website"]]:
      try:
        if element_name == "product":
          continue

        elif element_name == "product_image_urls":
          # WebDriverWait(driver, 120).until(EC.presence_of_element_located(get_selector(config["website"], element_name)))
          regex = r'(?:url\(")(.*)(?:"\))'
          WebDriverWait(driver, 120, ignored_exceptions=(NoSuchElementException,StaleElementReferenceException)).until(
            EEC.all_elements_have_attribute(get_selector(config["website"], element_name), "style")
          )
          driver.implicitly_wait(20)
          elements = driver.find_elements(*get_selector(config["website"], element_name))
          [ print(element.get_attribute("style")) for element in elements ]
          urls = [ re.search(regex, element.get_attribute("style")).group(1) for element in elements ]
          result[element_name] = ",".join(urls)
          
        else:
          WebDriverWait(driver, 60).until(EC.presence_of_element_located(get_selector(config["website"], element_name)))
          element = driver.find_element(*get_selector(config["website"], element_name))
          result[element_name] = element.text

      except:
        handle_exception()
      
    results.append(result)

  print(results)
  with open("products.csv", "w", encoding="utf_8_sig", newline="") as csvFile:
    csvFile.write("sep=@\n")
    field_names = [ field_name for field_name in list(element_name_to_field_name.values()) ]
    csvWriter = csv.DictWriter(csvFile, fieldnames=field_names, delimiter="@")
    csvWriter.writeheader()

    for result in results:
      row = { 
        element_name_to_field_name[element_name]: result[element_name] 
        for element_name in result 
        if element_name != "product_rating" and element_name != "product_rating_ammount" 
      }
      pprint(row)
      # print(set(row.keys()))
      # print(set(field_names))
      # print(f'{set(row.keys()) == set(field_names)}')
      csvWriter.writerow({ 
        element_name_to_field_name[element_name]: result[element_name] 
        for element_name in result 
        if element_name != "product_rating" and element_name != "product_rating_ammount" 
      })

except:
  handle_exception()
finally:
  driver.minimize_window()
  input("\n\n\nEnter to quit\n\n\n")
  driver.quit()