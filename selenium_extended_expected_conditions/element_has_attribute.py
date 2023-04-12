class element_has_attribute:
  def __init__(self, selector, attribute_name):
    self._selector = selector
    self._attribute_name = attribute_name


  def __call__(self, driver):
    element = driver.find_element(*self._selector)
    if element.get_attribute(self._attribute_name) == "":
      return False
    return element