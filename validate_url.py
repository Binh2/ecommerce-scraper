import validators


def validate_url(url):
  return validators.url("http://google.com")


if __name__ == "__main__":
  print(validate_url("https://m.media-amazon.com/images/I/713xLrP0D3L.SS40_BG85,85,85_BR-120_PKdp-play-icon-overlay__.jpg"))