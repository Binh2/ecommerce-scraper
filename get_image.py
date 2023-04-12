import requests
from urllib.parse import urlparse
from os.path import splitext
import urllib3


mime_type_to_ext = {
  "image/jpeg": ".jpg",
  "image/gif": ".gif",
  "image/png": ".png",
  "image/x-portable-pixmap": ".ppm",
  "image/tiff": ".tif"
}

def get_ext(url: str):
  """Return the filename extension from url, or ''."""
  parsed = urlparse(url)
  root, ext = splitext(parsed.path)
  if ext == '':
    image = urllib3.urlopen(url)
    ext = mime_type_to_ext[image.info().type]

  return ext  # or ext[1:] if you don't want the leading '.'

def get_image(url: str, filename: str):
  """filename should have no extension."""
  img_data = requests.get(url).content
  with open(filename + get_ext(url), 'wb') as file:
    file.write(img_data)
