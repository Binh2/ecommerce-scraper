from selenium.webdriver.common.by import By
import constants


class SelectorsConstant:
  def __init__(self, website: str, additional_info: bool = False):
    self._SELECTORS = constants.SELECTORS
    self._default_values = {
      "multiple_elements": False,
      "selector_type": By.CSS_SELECTOR,
      "selector": "",
      "attribute": "",
      "concatenate_function": lambda x: x,
      "transform_function": lambda x: x,
      "action": "get",
    }
    self._website = website
    self._additional_info = additional_info
    self.setUp(dict(self._SELECTORS[self._website]))
  
  def setUp(self, selectors):
    '''Recursively iterate through selectors to add nested selectors to the self._SELECTORS'''
    for element_name, selector_info in selectors.items():
      if element_name.startswith("product"):
        if type(selector_info) == str:
          self._SELECTORS[self._website][element_name] = selector_info
          continue
        
        self._SELECTORS[self._website][element_name] = selector_info
        self.setUp(selector_info)

  def __getitem__(self, element_name: str):
    if isinstance(self._SELECTORS[self._website][element_name], str):
      if self._additional_info:
        return (By.CSS_SELECTOR, self._SELECTORS[self._website][element_name], self._default_values)
      return (By.CSS_SELECTOR, self._SELECTORS[self._website][element_name])
    
    selector_info = self._SELECTORS[self._website][element_name]
    temp_selector_info = dict(self._default_values)
    temp_selector_info.update(selector_info)
    if self._additional_info:
      return (temp_selector_info["selector_type"], temp_selector_info["selector"], temp_selector_info)
    return (temp_selector_info["selector_type"], temp_selector_info["selector"])
  
  def __iter__(self):
    return iter({element_name: self[element_name] for element_name in self._SELECTORS[self._website]})
  

# if __name__ == "__main__":
# from constant_processors import SelectorsConstant
# SELECTORS = SelectorsConstant("amazon")
# print(SELECTORS["product"])