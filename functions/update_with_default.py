def update_with_default(default_dict: dict, new_dict: dict) -> dict:
  '''Take in a default_dict and apply the new key value from new_dict to the default_dict'''
  temp_dict = dict(default_dict)
  temp_dict.update(new_dict)
  return temp_dict