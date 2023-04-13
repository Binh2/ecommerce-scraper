class Test():
  def __getitem__(self, *args):
    return sum(*args)

test = Test()
print(test[3,4,5])