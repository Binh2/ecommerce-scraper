from selenium.webdriver.common.by import By
import constants


class SelectorsConstant:
  def __init__(self, website: str, additional_info: bool = False):
    self._SELECTORS = dict(constants.SELECTORS)
    self._default_values = {
      "multiple_elements": False,
      "selector_type": By.CSS_SELECTOR,
      "selector": "",
      "attribute": "",
      "concatenate_function": lambda x: x,
      "transform_function": lambda x: x,
      "action": "get",
      "is_descendant": False,
    }
    self._website = website
    self._additional_info = additional_info
    self.traverse(self._SELECTORS[self._website], self.addDefault)
    # self.setUp(dict(self._SELECTORS[self._website]))
  
  def traverse(self, selectors, callback):
    for element_name, selector_info in selectors.items():
      callback(selectors, element_name)
      if not isinstance(selector_info, dict):
        continue
      
      self.traverse(selectors[element_name].get("children", {}), callback)
  
  def traverse_with_return(self, selectors: dict, callback: callable):
    for element_name, selector_info in selectors.items():
      result = callback(selectors, element_name)
      if result != None:
        return result
      
      if not isinstance(selector_info, dict):
        continue
      
      result = self.traverse_with_return(selectors[element_name].get("children", {}), callback)
      if result != None:
        return result

  def addDefault(self, selectors, element_name):
    selector_info = {}
    if isinstance(selectors[element_name], str):
      selector_info["selector"] = selectors[element_name]
    else:
      selector_info = selectors[element_name]
    temp_selector_info = dict(self._default_values)
    temp_selector_info.update(selector_info)
    selectors[element_name] = temp_selector_info

  def _get_item(self, selectors, element_name: str):
    return selectors.get(element_name, None)

  def __getitem__(self, element_name: str):
    return self.traverse_with_return(self._SELECTORS[self._website], lambda selectors, _: self._get_item(selectors, element_name))
  
  def __iter__(self):
    return iter({element_name: self[element_name] for element_name in self._SELECTORS[self._website]})
  

# if __name__ == "__main__":
# from constant_interpreters import SelectorsConstant
# SELECTORS = SelectorsConstant("amazon")
# print(SELECTORS["product"])