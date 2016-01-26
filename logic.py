def isFieldsExist(data, list_fields):
    """Returns true if list_fields are all fields in data, else False."""
    for field in list_fields:
      if field not in data:
            return False
    return True
