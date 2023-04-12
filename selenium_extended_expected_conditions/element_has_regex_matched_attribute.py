import re


class element_has_regex_matched_attribute:
  def __init__(self, selector, attribute_name, regex):
    self._selector = selector
    self._attribute_name = attribute_name
    self._regex = regex


  def __call__(self, driver):
    element = driver.find_element(*self._selector)
    if re.match(self._regex, element.get_attribute(self._attribute_name)) == None:
      return False
    return element