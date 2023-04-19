from urllib.parse import quote, urlparse


def encode_url(url):
  ''' Encode url so url doesn't have white space and commas.'''
  # <scheme>://<netloc>/<path>;<params>?<query>#<fragment>
  parsed = urlparse(url)
  scheme_netloc = f'{parsed.scheme}://{parsed.netloc}'
  rest = f'{parsed.path}{";"+parsed.params if parsed.params else ""}{"?"+parsed.query if parsed.query else ""}{"#"+parsed.fragment if parsed.fragment else ""}'
  return scheme_netloc + quote(rest)


if __name__ == "__main__":
  print(encode_url("https://m.media-amazon.com/images/I/713xLrP0D3L.SS40_BG85,85,85_BR-120_PKdp-play-icon-overlay__.jpg"))