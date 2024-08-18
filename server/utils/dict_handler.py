import copy

def destruct(dict, keys: type[list[str]]):
    """
    destruct method is used to destructuring a dictionary object
    """
    cloned = copy.deepcopy(dict)
    keys = tuple(keys)
    values = []
    for k in keys:
        if k in cloned:
            values.append(cloned[k])
            del cloned[k]
    if '*' in keys:
        values.append(cloned)
    return tuple(values)
