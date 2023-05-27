import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
import constant_interpreters
import selenium_extended_expected_conditions as EEC
import functions

class SelectorsProcessor:
  def __init__(self, driver: WebDriver, website: str, delay = 60, 
  ignored_element_names = ['product', 'product_next_page']):
    self._driver = driver
    self._ignored_element_names = ignored_element_names
    self._website = website
    self._delay = delay
    self._SELECTORS = constant_interpreters.SelectorsConstant(website)
    self._EXTENDED_SELECTORS = constant_interpreters.SelectorsConstant(website, additional_info=True)
    self._REGEXES = constant_interpreters.RegexesConstant(website)
    self._EXTENDED_REGEXES = constant_interpreters.RegexesConstant(website, additional_info=True)

  def process_attribute(self, element: WebElement, attribute: str):
    text = None
    if attribute == "":
      text = element.text
    else:
      text = element.get_attribute(attribute)
    
    assert(text != None)
    return text

  def process_regex(self, element_name: str, text: str):
    ''' Do regex subtitute or search or validate. Currently, only do subtitution.'''
    processed_text = None
    # if regex_info["regex_type"] == "sub":
    
    regex = self._REGEXES[element_name]
    if isinstance(regex, list):
      processed_text = text
      for regex_ in regex:
        processed_text = re.sub(*regex_, processed_text)
    else:
      processed_text = re.sub(*regex, text)
    print(processed_text)
    return processed_text
  
  def process_action(self, element: WebElement, element_name: str):
    '''Only process click and hover'''
    selector_info = self._EXTENDED_SELECTORS[element_name][2]
    action = selector_info["action"]
    if action == "click":
      element.click()
    elif action == "hover":
      functions.hover_over_element(self._driver, element)
  
  def process_element_index(self, elements: list[WebElement]):
    element_index = self._selector_info["element_index"]
    if element_index != None:
      return [elements[element_index]]
    return elements

  def process_scroll(self):
    if self._selector_info['action'] == 'scroll,get':
      self._driver.execute_script("window.scrollTo(0, 1000)")

  def __call__(self, element_name: str):
    print(element_name)
    if element_name in self._ignored_element_names:
      return None

    if self._website == 'lazada':
      if element_name == 'product_thumpnail_image_urls':
        return self.process_lazada_product_thumpnail_image_urls()
      elif element_name == 'product_image_url': 
        return None
    
    selector_info = self._EXTENDED_SELECTORS[element_name][2]
    self._selector_info = selector_info
    self.process_scroll()
    WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located(self._SELECTORS[element_name]))
    

    # Get text/attribute string from element(s)
    text = None
    if selector_info["is_multiple_elements"]:
      texts = []
      elements = self._driver.find_elements(*self._SELECTORS[element_name])
      elements = self.process_element_index(elements)
      if selector_info["action"] in ["click", "hover"]:
        for element in elements:
          try:
            self.process_action(element, element_name)
            
          except TimeoutException:
            pass
          except:
            functions.handle_exception()
      
      elif selector_info["action"] in ["get", "scroll,get"]:
        print(elements)
        texts = [ self.process_attribute(element, selector_info["attribute"]) for element in elements ]
      text = selector_info["concatenate_function"](texts)
    else:
      element = self._driver.find_element(*self._SELECTORS[element_name])
      text = self.process_attribute(element, selector_info["attribute"])
    assert(text != None)

    processed_text = self.process_regex(element_name, text)

    # Use a function to transform text
    transformed_text = selector_info["transform_function"](processed_text)
    return transformed_text

  def run(self):
    result = {}
    for element_name in self._SELECTORS:
      try:
        text = self(element_name)
        if text == None:
          continue
        result[element_name] = text

      except:
        functions.handle_exception()
    return result

  def process_lazada_product_thumpnail_image_urls(self):
    element_name = 'product_thumpnail_image_urls'
    WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located(self._SELECTORS[element_name]))
    selector_info = self._EXTENDED_SELECTORS[element_name][2]
    self._selector_info = selector_info

    text = None
    if selector_info["is_multiple_elements"]:
      elements = self._driver.find_elements(*self._SELECTORS[element_name])
      elements = self.process_element_index(elements)
      texts = []
      if selector_info["action"] in ["click", "hover"]:
        for element in elements:
          try:
            self.process_action(element, element_name)
            text = self.process_lazada_product_image_url()
            texts.append(text)
            
          except TimeoutException:
            pass
          except:
            functions.handle_exception()
            
      text = selector_info["concatenate_function"](texts)
    assert(text != None)
    processed_text = self.process_regex(element_name, text)

    # Use a function to transform text
    transformed_text = selector_info["transform_function"](processed_text)
    return transformed_text
      
  def process_lazada_product_image_url(self):
    element_name = 'product_image_urls'
    WebDriverWait(self._driver, self._delay).until(EC.presence_of_element_located(self._SELECTORS[element_name]))
    selector_info = self._EXTENDED_SELECTORS[element_name][2]

    text = None
    if not selector_info["is_multiple_elements"]:
      element = self._driver.find_element(*self._SELECTORS[element_name])
      text = self.process_attribute(element, selector_info["attribute"])
      assert(text != None)

    processed_text = self.process_regex(element_name, text)

    # Use a function to transform text
    transformed_text = selector_info["transform_function"](processed_text)
    return transformed_text