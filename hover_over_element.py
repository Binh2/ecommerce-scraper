from selenium.webdriver.common.action_chains import ActionChains


def hover_over_element(driver, element):
  a = ActionChains(driver)
  a.move_to_element(element).perform()