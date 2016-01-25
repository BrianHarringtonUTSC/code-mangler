def isFieldsExist(data, list_fields):
    for field in list_fields:
        if field not in data:
            return False
    return True
