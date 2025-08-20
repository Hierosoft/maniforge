
def encVal(v):
    '''
    Get the encoded value as would appear in Python code.
    '''
    if v is None:
        return "None"
    if v is True:
        return "True"
    if v is False:
        return "False"
    elif isinstance(v, str):
        return '"{}"'.format(v)
    return str(v)
