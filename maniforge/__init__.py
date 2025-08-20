#!/usr/bin/env python3
'''
maniforge
----------
by Poikilos
'''
from __future__ import print_function
from decimal import Decimal
import re

def cast_by_type_string(value, type_str):
    if value is None:
        return None
    elif value == "":
        return None
    # NOTE: to reverse this, you'd have to use type(var).__name__
    if type_str == "int":
        return int(value)
    elif type_str == "Decimal":
        return Decimal(value)
    elif type_str == "float":
        return float(value)
    elif type_str == "bool":
        return bool(value)
    else:
        return value


_digit_pattern = re.compile(r'\d')

def has_numbers(inputString):
    return bool(_digit_pattern.search(inputString))

