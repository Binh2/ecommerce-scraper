from typing import Any
from selenium.webdriver.common.by import By
import constants
from selectors_.constants import SELECTORS


class SelectorsConstant:
  def __init__(self, website: str, additional_info: bool = False):
    self._SELECTORS = dict(SELECTORS)
    self._default_values = {
      "is_multiple_elements": False,
      "selector_type": By.CSS_SELECTOR,
      "selector": "",
      "attribute": "",
      "concatenate_function": lambda x: x,
      "transform_function": lambda x: x,
      "action": "get",
      "children": None,
      "element_index": None,
    }
    self._website = website
    self._additional_info = additional_info
    self.traverse_with_return(self._SELECTORS[self._website], self.add_default)
  
  def traverse(self, selectors: dict[str, dict | Any], callback: callable):
    for element_name, selector_info in selectors.items():
      callback(selectors, element_name)
      if not isinstance(selector_info, dict):
        continue
      
      self.traverse(selectors[element_name].get("children", {}), callback)
  
  def traverse_with_return(self, selectors: dict[str, dict | Any], callback: callable):
    if selectors == None:
      return None
    
    for element_name, selector_info in selectors.items():
      result = callback(selectors, element_name)
      if result != None:
        return result
      
      if not isinstance(selector_info, dict):
        continue
      
      result = self.traverse_with_return(selectors[element_name].get("children", {}), callback)
      if result != None:
        return result

  def add_default(self, selectors: dict[str, dict | str | Any], element_name: str):
    selector_info = {}
    if isinstance(selectors[element_name], str):
      selector_info["selector"] = selectors[element_name]
    else:
      selector_info = selectors[element_name]
    temp_selector_info = dict(self._default_values)
    temp_selector_info.update(selector_info)
    selectors[element_name] = temp_selector_info

  def _get_item(self, selectors: dict[str, Any], element_name: str):
    return selectors.get(element_name, None)

  def __getitem__(self, element_name: str):
    result = self.traverse_with_return(self._SELECTORS[self._website], lambda selectors, _: self._get_item(selectors, element_name))
    selector = (result["selector_type"], result["selector"])
    if self._additional_info:
      return (*selector, result)
    return selector
  
  def __iter__(self):
    return iter({element_name: self[element_name] for element_name in self._SELECTORS[self._website]})
  

# if __name__ == "__main__":
# from constant_interpreters import SelectorsConstant
# SELECTORS = SelectorsConstant("amazon")
# print(SELECTORS["product"])