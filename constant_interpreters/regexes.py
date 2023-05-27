from pprint import pprint
from typing import Any
from constants import REGEXES
import functions


class RegexesConstant:
  def __init__(self, website: str, additional_info: bool = False):
    self._REGEXES = REGEXES
    self._website = website
    self._additional_info = additional_info
    self._default_values = {
      "regex_type": "sub",
      "regex": '',
      "replace": '',
    }
    self.traverse(REGEXES[self._website], self.add_default)

  def traverse(self, regexes: dict[str, dict | Any], callback: callable):
    for element_name, selector_info in regexes.items():
      callback(regexes, element_name)
      if not isinstance(selector_info, dict):
        continue
      
      self.traverse(regexes[element_name].get("children", {}), callback)

  def traverse_with_return(self, regexes: dict[str, dict | Any], callback: callable):
    if regexes == None:
      return None
    
    for element_name, regex_info in regexes.items():
      result = callback(regexes, element_name)
      if result != None:
        return result
      
      if not isinstance(regex_info, dict):
        continue
      
      result = self.traverse_with_return(regexes[element_name].get("children", {}), callback)
      if result != None:
        return result
  
  def add_default(self, regexes: dict[str, dict | str | Any], element_name: str):
    regex_info = {}
    if isinstance(regexes[element_name], list):
      # print(regexes[element_name])
      temp_regexes = []
      for i, regex_info in enumerate(regexes[element_name]):
        if isinstance(regex_info, str):
          regex_info["regex"] = regex_info
        
        # print(f'{i=} {self._default_values=} {regex_info=}')
        # regexes[element_name][i] = functions.update_with_default(self._default_values, regex_info)
        temp_regexes.append(functions.update_with_default(self._default_values, regex_info))
      regexes[element_name] = temp_regexes
      return

    elif isinstance(regexes[element_name], str):
      regex_info["regex"] = regexes[element_name]
    else:
      regex_info = regexes[element_name]
    regexes[element_name] = functions.update_with_default(self._default_values, regex_info)

  def _get_item(self, regexes: dict[str, Any], element_name: str):
    return regexes.get(element_name, None)

  def __getitem__(self, element_name: str):
    result = self.traverse_with_return(self._REGEXES[self._website], lambda regexes, _: self._get_item(regexes, element_name))
    if result == None:
      result = self._default_values
    
    regex = None
    if isinstance(result, list):
      regexes = []
      for result_ in result:
        regex = (result_["regex"], result_["replace"])
        if self._additional_info:
          regexes.append((*regex, result_))
        regexes.append(regex)
      return regexes
      
    else:
      regex = (result["regex"], result["replace"])
      if self._additional_info:
        return (*regex, result)
      return regex
  
  def __iter__(self):
    return iter([self[element_name] for element_name in self._REGEXES[self._website]])