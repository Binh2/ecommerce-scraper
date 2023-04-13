from selenium.webdriver.common.by import By
from constants import URLS


class UrlsContant:
  def __init__(self, website: str):
    self._URLS = URLS
    self._website = website

  def __getitem__(self, url_name: str):
    return self._URLS[self._website][url_name]
  
  def __iter__(self):
    return iter([self[url_name] for url_name in self._URLS[self._website]])