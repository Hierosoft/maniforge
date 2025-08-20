#!/usr/bin/env python3
'''
maniforge
----------
by Poikilos
'''
from __future__ import print_function
from decimal import Decimal
import os
import re
import sys
import pathlib
import shutil
import shlex
import git
import platform
from git import Repo

from subprocess import (
    Popen,
)

from .find_pycodetool import pycodetool  # noqa: F401
# ^ also works for submodules since changes sys.path
from .find_hierosoft import hierosoft
# ^ also works for submodules since changes sys.path

# from hierosoft.logging import (
#     to_syntax_error,  # (path, lineN, msg, col=None)
#     echo_SyntaxWarning,  # (path, lineN, msg, col=None)
#     raise_SyntaxError,  # (path, lineN, msg, col=None)
# )


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

