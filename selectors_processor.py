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
    self.ignored_element_names = ignored_element_names
    self.delay = delay
    self.SELECTORS = constant_interpreters.SelectorsConstant(website)
    self.EXTENDED_SELECTORS = constant_interpreters.SelectorsConstant(website, additional_info=True)
    self.REGEXES = constant_interpreters.RegexesConstant(website)
    self.EXTENDED_REGEXES = constant_interpreters.RegexesConstant(website, additional_info=True)

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
    
    regex = self.REGEXES[element_name]
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
    selector_info = self.EXTENDED_SELECTORS[element_name][2]
    action = selector_info["action"]
    if action == "click":
      element.click()
    elif action == "hover":
      functions.hover_over_element(self._driver, element)
  
  def process_element_index(self, elements: list[WebElement]):
    element_index = self._selector_info["element_index"]
    if element_index != None:
      elements = [elements[element_index]]

  def __call__(self, element_name: str):
    print(element_name)
    if element_name in self.ignored_element_names:
      return None

    else:
      WebDriverWait(self._driver, self.delay).until(EC.presence_of_element_located(self.SELECTORS[element_name]))
      selector_info = self.EXTENDED_SELECTORS[element_name][2]
      self._selector_info = selector_info

      # Get text/attribute string from element(s)
      text = None
      if selector_info["is_multiple_elements"]:
        texts = []
        elements = self._driver.find_elements(*self.SELECTORS[element_name])
        elements = self.process_element_index(elements)
        if selector_info["action"] in ["click", "hover"]:
          if selector_info["children"] != None:
            previous_attribute = ""
            for element_name2 in selector_info["children"]:
              for element in elements:
                try:
                  self.process_action(element, element_name)
                  WebDriverWait(self._driver, self.delay).until(EEC.element_attribute_changed(self.SELECTORS[element_name], selector_info["attribute"], previous_attribute))
                  previous_attribute = element.get_attribute(selector_info["attribute"])
                  texts.append(self(element_name2))
                except TimeoutException:
                  pass
                except:
                  functions.handle_exception()
                finally:
                  print(texts)
        
        elif selector_info["action"] == "get":
          texts = [ self.process_attribute(element, selector_info["attribute"]) for element in elements ]
        text = selector_info["concatenate_function"](texts)
      else:
        element = self._driver.find_element(*self.SELECTORS[element_name])
        text = self.process_attribute(element, selector_info["attribute"])
      assert(text != None)

      processed_text = self.process_regex(element_name, text)

      # Use a function to transform text
      transformed_text = selector_info["transform_function"](processed_text)
      return transformed_text
