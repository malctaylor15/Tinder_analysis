# Utility functions to be used across scripts

import numpy as np
from decimal import Decimal

def default(o):
    if isinstance(o, np.int64): return int(o)
    raise TypeError

def check_dict_types(dirty_dict):
    """
    Changes data types of dictionaries so they can be serialized/ uploaded to dynamo

    Input
    dirty_dict (dict)
        Raw dictionary with mixed data types

    Returns
    dirty_dict (dict)
        Dictionary with non serializable data types removed

    """
    for k, val in dirty_dict.items():
        if isinstance(val, np.int64):
            dirty_dict[k] = int(val)
        elif (type(val) == np.float64):
            dirty_dict[k] = Decimal(str(val))
        elif type(val) == dict:
            check_dict_types(val)
    return(dirty_dict)

