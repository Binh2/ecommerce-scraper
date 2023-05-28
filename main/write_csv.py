import csv
import constants
from pprint import pprint


def write_csv(results):
  '''Write to CSV file'''
  ignored_element_names = ["product_rating", "product_rating_amount"]
  with open("products.csv", "w", encoding="utf_8", newline="") as csvFile:
    # csvFile.write("sep=@\n") # Uncomment this if you want to view it in excel (but can't import into wordpress)
    field_names = [ field_name for field_name in list(constants.element_name_to_csv_field_name.values()) ]
    csvWriter = csv.DictWriter(csvFile, fieldnames=field_names, delimiter="@")
    csvWriter.writeheader()

    for result in results:
      row = { 
        constants.element_name_to_csv_field_name[element_name]: result[element_name] 
        for element_name in result 
        # if not element_name in ignored_element_names
      }
      pprint(row)
      csvWriter.writerow(row)