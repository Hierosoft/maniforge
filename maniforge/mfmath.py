

from decimal import Decimal
import math


def show_fewest(n):
    '''
    Display only decimal places that are not 0.

    Sequential arguments:
    n -- a float/Decimal value.
    '''
    s = "{}".format(n)
    while s.endswith(".0") or s.endswith("0"):
        s = s[:-1]
    return s



def round_up(n, decimals=0):
    # See <https://realpython.com/python-rounding/
    #   #:~:text=To%20implement%20the%20%E2%80%9Crounding%20up,
    #   equal%20to%20a%20given%20number.>
    multiplier = 10 ** decimals
    return math.ceil(n * multiplier) / multiplier


python_round = round


def round_nearest_d(*args):
    '''
    This is a Decimal version of round_nearest. See round_nearest for
    documentation.
    '''
    if len(args) == 1:
        x = args[0]
        i, f = divmod(x, 1)
        return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))
    elif len(args) == 2:
        if not isinstance(args[1], int):
            raise TypeError("precision must be an int.")
        precision = args[1]
        # return python_round(args[0], precision)
        multiplier = Decimal(10 ** precision)
        x = args[0]
        if isinstance(x, float):
            x = Decimal(x)
        if not isinstance(x, Decimal):
            raise TypeError("The value must be a float or Decimal.")
        increased = Decimal(x * multiplier)
        return Decimal(round_nearest_d(increased)) / Decimal(multiplier)
    else:
        ValueError(
            "round_nearest only takes 1 or 2 arguments:"
            " (value [, precision])"
        )


def round_nearest(*args):
    '''
    This function circumvents the new Python 3 behavior where round uses
    "banker's rounding" to "limit the accumulation of errors when
    summing a list of rounded integers" (according to remi.lapeyre on
    <https://bugs.python.org/issue36082>).
    - The result of banker's rounding is that round(1.5) is 2 and
      round(2.5) is 2 and round(2.51) is 3. Rounding even numbers
      differs since the rounding is toward (but not all the way to) the
      nearest even number.
    - To monkey patch Python 3 to do rounding the "school" way (such as
      rounding 2.5 to 3), do:
      round = round_nearest

    This function is based on E. Zeytinci's Nov 13, 2019 answer
    <https://stackoverflow.com/a/58839239> on
    <https://stackoverflow.com/questions/58838995/how-to-switch-off-
    bankers-rounding-in-python>.

    However, this version skips the procedure if a second sequential
    argument is given.

    Sequential arguments:
    value -- a float value to round.
    precision (optional) -- the number of decimal places to keep (uses
        Python's builtin round function which uses banker's rounding in
        Python 3). If not provided, value is rounded to a whole number
        manually (without Python's builtin round function).
    '''
    if len(args) == 1:
        x = args[0]
        i, f = divmod(x, 1)
        return int(i + ((f >= 0.5) if (x > 0) else (f > 0.5)))
    elif len(args) == 2:
        precision = args[1]
        if not isinstance(args[1], int):
            raise ValueError("precision must be an int.")
        # return python_round(args[0], precision)
        multiplier = 10 ** precision
        increased = args[0] * multiplier
        return round_nearest(increased) / multiplier
    else:
        ValueError(
            "round_nearest only takes 1 or 2 arguments:"
            " (value [, precision])"
        )

round = round_nearest


def getHMSFromS(estSec):
    estLeft = estSec
    estHr = estLeft // 3600
    estLeft -= float(estHr) * 3600.0
    estMin = estLeft // 60
    estLeft -= float(estMin) * 60.0
    estLeft = round(estLeft)
    return int(estHr), int(estMin), round(estLeft)


def getHMSMessageFromS(estSec):
    h, m, s = getHMSFromS(estSec)
    return "{}h{}m{}s".format(h, m, s)

