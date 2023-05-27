from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import functions

chrome_options = Options()
# chrome_options.add_argument('--headless')
chrome_options.add_argument('--log-level=3')
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(r'https://www.amazon.com/ECOVACS-Self-Empty-Auto-Clean-Navigation-Avoidance/dp/B0BBYWK3HY/ref=sr_1_1_sspa?crid=1GRA6E7EMRX3J&keywords=robot%2Bh%C3%BAt%2Bb%E1%BB%A5i&qid=1682342160&sprefix=robot%2Bh%C3%BAt%2Bbui%2Caps%2C541&sr=8-1-spons&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFMQlo0RE1OUFoyRFAmZW5jcnlwdGVkSWQ9QTA3NTAzNDUyQUFXMEVFM0pGTFdZJmVuY3J5cHRlZEFkSWQ9QTAzODgwMjkyOUkxNU4xWUZWQVBUJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ&th=1')
thumpnail_image = driver.find_elements(By.CSS_SELECTOR, '.item.imageThumbnail')[3]
functions.hover_over_element(driver, thumpnail_image)
driver.maximize_window()
input("Enter to quit")