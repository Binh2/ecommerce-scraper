from selenium.webdriver.common.by import By
from constants import SELECTORS


class SelectorsContant:
  def __init__(self, website: str, additional_info: bool = False):
    self._SELECTORS = SELECTORS
    self._default_values = {
      "multiple_elements": False,
      "selector_type": By.CSS_SELECTOR,
      "selector": "",
      "attribute": "",
      "concatenate_function": lambda x: x,
      "transform_function": lambda x: x,
    }
    self._website = website
    self._additional_info = additional_info

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