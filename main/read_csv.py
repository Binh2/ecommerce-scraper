import csv


def read_csv():
  results = []
  with open("products.csv", "w", encoding="utf_8", newline="") as file:
    csvReader = csv.DictReader(file)

    for result in csvReader:
      results.append(result)

  return results