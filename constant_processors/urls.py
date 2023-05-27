from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
import constant_interpreters
import functions


class UrlsProcessor():
  def __init__(self, driver: WebDriver, website: str, keyword: str, number_of_products: int, delay: int) -> None:
    self._driver = driver
    self._website = website
    self._keyword = keyword
    self._number_of_products = number_of_products
    self._delay = delay * 2
    
    self._URLS = constant_interpreters.UrlsConstant(website)
    self._SELECTORS = constant_interpreters.SelectorsConstant(website)
    self._EXTENDED_SELECTORS = constant_interpreters.SelectorsConstant(website, additional_info=True)
    self._REGEXES = constant_interpreters.RegexesConstant(website)
    self._EXTENDED_REGEXES = constant_interpreters.RegexesConstant(website, additional_info=True)

  def run(self):
    '''Get all the product urls'''
    product_urls = []
    try:
      i = self._URLS["page_index"]
      while len(product_urls) < self._number_of_products:
        WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located(self._SELECTORS["product"]))
        product_elements = iter(self._driver.find_elements(*self._SELECTORS["product"]))
        self._selector_info = self._EXTENDED_SELECTORS["product"][2]
        while len(product_urls) < self._number_of_products:
          try:
            product_element = next(product_elements)
          except StopIteration:
            break
          
          if self._selector_info["attribute"] == "":
            product_urls.append(product_element.text)
          else:
            product_urls.append(product_element.get_attribute(self._selector_info["attribute"]))

        self.process_next_page(i)
        i += 1

    except TimeoutException:
      print("Products page is not opening")
    assert(product_urls != [])
    print(f'{product_urls=}')
    return product_urls

  def process_next_page(self, page_index: int):
    if self._website == 'lazada':
      next_page_url = self._URLS["next_page"] % {"keyword": self._keyword, "page_index": str(page_index)}
      self._driver.get(next_page_url)
      return
    next_page_button = WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located(self._SELECTORS["product_next_page"]))      
    next_page_button.click()  
