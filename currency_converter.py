import requests
import json
import datetime
import constants


class CurrencyConvertor:
  def __init__(self, api_key: str = constants.CURRENCY_CONVERTER_API_KEY, from_currency: str = "USD", to_currency: str = "VND", update_interval: int = 1, verbose: bool = False):
    '''Get fixer api data from 'https://api.apilayer.com' and save it in the self.filename.

    Input:
      api_key: get from 'https://api.apilayer.com' for fixer api.
      from_currency: get from the keys in currency_symbols.py or can be query using the fixer api.
      to_currency: get from the keys in currency_symbols.py or can be query using the fixer api.
      update_interval (in days): The interval to update the self.filename.'''
    self._url = f'https://api.apilayer.com/fixer/latest?base={from_currency}&symbols={to_currency}'
    self.from_currency = from_currency
    self.to_currency = to_currency
    self.filename = f'{from_currency}_to_{to_currency}.json'
    self.api_key = api_key
    self.update_inteval = update_interval
    self.verbose = verbose
    
    try:
      self._data = self._get_data_from_file()
      if datetime.date.today() - datetime.date.fromtimestamp(self._data["timestamp"]) >= datetime.timedelta(days=update_interval):
        self._data = self._get_data_from_url()
        self._save_data()
      
    except FileNotFoundError:
      if verbose: print("Getting currency converter data...")
      self._data = self._get_data_from_url()
      self._save_data()

    except:
      self._data = self._get_default_data()

    finally:
      try:
        if verbose: print(f'{self._data=}')
        self.rates = self._data["rates"]
      except:
        self._data = self._get_default_data()

  def _get_data_from_file(self):
    result = {}
    with open(self.filename) as json_file:
      result = json.load(json_file)
    return result
  
  def _get_data_from_url(self):
    return requests.get(self._url, headers={ "apikey": self.api_key }).json()
  
  def _get_default_data(self):
    if self.from_currency == "USD" and self.to_currency == "VND":
      return {
        "success": True,
        "timestamp": 1681874824,
        "base": "USD",
        "date": "2023-04-19",
        "rates": {
          "VND": 23504
        }
      }
    elif self.from_currency == "VND" and self.to_currency == "USD":
      return {
        "success": True,
        "timestamp": 1681874824,
        "base": "VND",
        "date": "2023-04-19",
        "rates": {
          "USD": 23504
        }
      }
  
  def _save_data(self):
    with open(self.filename, "w") as json_file:
      json.dump(self._data, json_file)

  def convert(self, amount):
    return amount * self.rates[self.to_currency]
  
  def convert_back(self, amount):
    return amount / self.rates[self.to_currency]
  
  def __call__(self, amount):
    return self.convert(amount)
 
# Driver code
if __name__ == "__main__":
  usd_to_vnd = CurrencyConvertor()
  amount = 1
  print(usd_to_vnd(amount))
