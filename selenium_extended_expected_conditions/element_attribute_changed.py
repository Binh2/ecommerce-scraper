from selenium.webdriver.chrome.webdriver import WebDriver


class element_attribute_changed:
  def __init__(self, selector: tuple[str, str], attribute_name: str, previous_attribute: str):
    self._selector = selector
    self._attribute_name = attribute_name
    self._previous_attribute = previous_attribute


  def __call__(self, driver: WebDriver):
    element = driver.find_element(*self._selector)
    if element.get_attribute(self._attribute_name) == self._previous_attribute:
      return False
    return element