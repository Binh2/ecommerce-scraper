class all_elements_have_attribute:
  def __init__(self, selector, attribute_name):
    self._selector = selector
    self._attribute_name = attribute_name


  def __call__(self, driver):
    elements = driver.find_elements(*self._selector)
    if all([ element.get_attribute(self._attribute_name) != "" for element in elements ]):
      return elements
    return False