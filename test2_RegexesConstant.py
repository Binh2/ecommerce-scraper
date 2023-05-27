from pprint import pprint
import constant_interpreters
from types import GeneratorType


website = "amazon"
REGEXES = constant_interpreters.RegexesConstant(website)
pprint(REGEXES._REGEXES)
result = REGEXES["product_regular_price"]
print(result)
pprint(list(result) if isinstance(result, GeneratorType) else result)