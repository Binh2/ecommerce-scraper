URLS = {
  'shopee': {
    'base': 'https://shopee.vn', # Currently useless
    'search': 'https://shopee.vn/search?keyword=',
  },
  'amazon': {
    'base': 'https://www.amazon.com',
    'search': 'https://www.amazon.com/s?k='
  },
  'lazada': {
    'base': 'https://www.lazada.vn',
    'search': 'https://www.lazada.vn/tag/robot-hut-bui/?q=',
    'page_index': 1,
    'next_page': 'https://www.lazada.vn/tag/robot-hut-bui/?page=%(page_index)s&q=%(keyword)s',
  },
}