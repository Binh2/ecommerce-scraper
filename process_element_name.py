from operator import itemgetter
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium.webdriver.support import expected_conditions as EC
from hover_over_element import hover_over_element


def process_element_name(driver, element_name, **CONSTANTS):
  ignored_element_name, delay, SELECTORS, EXTENDED_SELECTORS, REGEXES, EXTENDED_REGEXES = itemgetter('ignored_element_name', 'delay', 'SELECTORS', 'EXTENDED_SELECTORS', 'REGEXES', 'EXTENDED_REGEXES')(CONSTANTS)
  if element_name in ignored_element_name:
    return

  else:
    WebDriverWait(driver, delay).until(EC.presence_of_element_located(SELECTORS[element_name]))
    selector_info = EXTENDED_SELECTORS[element_name][2]

    # Get text/attribute string from element(s)
    text = None
    if selector_info["multiple_elements"]:
      texts = []
      elements = driver.find_elements(*SELECTORS[element_name])
      elements_iter = iter(elements)

      if selector_info["action"] == "hover":
        for element_name2 in selector_info:
          if element_name2.startswith("product"):
            hover_over_element(driver, next(elements_iter))
            texts.append(process_element_name(driver, element_name, **CONSTANTS))
      
      elif selector_info["action"] == "get":
        if selector_info["attribute"] == "":
          texts = [ element.text for element in elements ]
        else:
          texts = [ element.get_attribute(selector_info["attribute"]) for element in elements ]
        text = selector_info["concatenate_function"](texts)
    else:
      element = driver.find_element(*SELECTORS[element_name])
      # print(f'{EXTENDED_SELECTORS[element_name]=}')
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

    # Use a function to transform text
    transformed_text = selector_info["transform_function"](processed_text)
  return transformed_text