import re


class all_elements_have_regex_matched_attribute:
  def __init__(self, selector, attribute_name, regex):
    self._selector = selector
    self._attribute_name = attribute_name
    self._regex = regex


  def __call__(self, driver):
    elements = driver.find_elements(*self._selector)
    if all([re.match(self._regex, element.get_attribute(self._attribute_name)) != None for element in elements]):
      return elements
    return False