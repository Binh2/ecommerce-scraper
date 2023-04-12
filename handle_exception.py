import traceback


def handle_exception():
  print(traceback.format_exc().split("Stacktrace:")[0])