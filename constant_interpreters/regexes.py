from handle_exception import handle_exception
from constants import REGEXES

class RegexesConstant:
  def __init__(self, website: str, additional_info: bool = False):
    self._REGEX = REGEXES
    self._website = website
    self._additional_info = additional_info
    self._default_values = {
      "regex_type": "sub",
      "regex": '',
      "replace": ''
    }

  def __getitem__(self, element_name: str):
    try:
      temp_result = dict(self._default_values)
      temp_result.update(self._REGEX[self._website][element_name])
      if self._additional_info:
        return (temp_result["regex"], temp_result["replace"], temp_result)
      return (temp_result["regex"], temp_result["replace"])
    except KeyError:
      pass
    except:
      handle_exception()
    
    if self._additional_info:
      return (self._default_values["regex"], self._default_values["replace"], self._default_values)
    return (self._default_values["regex"], self._default_values["replace"])
  
  def __iter__(self):
    return iter([self[element_name] for element_name in self._REGEX[self._website]])