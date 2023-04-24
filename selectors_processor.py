import re
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constant_interpreters
from hover_over_element import hover_over_element


class SelectorProcessor:
  def __init__(self, driver, website, ignored_element_names = ['product', 'product_next_page'], 
               delay = 60):
    self.driver = driver
    self.ignored_element_names = ignored_element_names
    self.delay = delay
    self.SELECTORS = constant_interpreters.SelectorsConstant(website)
    self.EXTENDED_SELECTORS = constant_interpreters.SelectorsConstant(website, additional_info=True)
    self.REGEXES = constant_interpreters.RegexesConstant(website)
    self.EXTENDED_REGEXES = constant_interpreters.RegexesConstant(website, additional_info=True)
  
  def process_action__hover(self, element_name):
    selector_info = self.EXTENDED_SELECTORS[element_name][2]
    if selector_info["action"] == "hover":
      for element_name2 in selector_info:
        self.process_children(element_name, lambda: hover_over_element(self.driver, ))

  def process_children(self, element_name, action_callback: callable):
    if element_name == "children":
      action_callback()
      self.texts = self.process_element_name(element_name)

  def process_element_name(self, element_name):
    if element_name in self.ignored_element_names:
      return

    else:
      WebDriverWait(self.driver, self.delay).until(EC.presence_of_element_located(self.SELECTORS[element_name]))
      selector_info = self.EXTENDED_SELECTORS[element_name][2]

      # Get text/attribute string from element(s)
      text = None
      if selector_info["multiple_elements"]:
        texts = []
        elements = self.driver.find_elements(*self.SELECTORS[element_name])
        elements_iter = iter(elements)

        if selector_info["action"] == "hover":
          for element_name2 in selector_info:
            if element_name2 == "children":
              hover_over_element(self.driver, next(elements_iter))
              texts.append(self.process_element_name(element_name))
        
        elif selector_info["action"] == "get":
          if selector_info["attribute"] == "":
            texts = [ element.text for element in elements ]
          else:
            texts = [ element.get_attribute(selector_info["attribute"]) for element in elements ]
          text = selector_info["concatenate_function"](texts)
      else:
        element = self.driver.find_element(*self.SELECTORS[element_name])
        # print(f'{self.EXTENDED_SELECTORS[element_name]=}')
        if selector_info["attribute"] == "":
          text = element.text
        else:
          text = element.get_attribute(selector_info["attribute"])
      assert(text != None)

      # Do regex (sub (subtitute) or search)
      processed_text = None
      regex_info = self.EXTENDED_REGEXES[element_name][2]
      # if regex_info["regex_type"] == "sub":
      processed_text = re.sub(*self.REGEXES[element_name], text)

      # Use a function to transform text
      transformed_text = selector_info["transform_function"](processed_text)
    return transformed_text
