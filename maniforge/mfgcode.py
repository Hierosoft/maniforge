

from decimal import Decimal
from logging import getLogger

from maniforge import has_numbers
from maniforge.mfmath import show_fewest

logger = getLogger(__name__)


def modify_cmd_meta(meta, key, value, precision=5):
    """Modify G-code command metadata.

    Args:
        meta (List[List[Any]]): A list of arguments (such as lexed &
            split by get_cmd_meta), where the first element is a command
            such as ['G', '1']
        key (str): Name of the argument to set, such as "S" in "S1".
        value (Any): The new value (such as "1" in "S1")
        precision (int, optional): Number of decimal places. Defaults to
            5.

    Raises:
        ValueError: If the key has no value in the original command.
            (so that value should not be changed, or should not be
            changed in that case).

    Returns:
        bool: True if could modify, False if not.
    """
    for pair in meta:
        if pair[0] != key:
            continue
        if len(pair) < 2:
            raise ValueError(
                "The key has no param in the original command `{}`,"
                " so the key '{}' was left unchanged for safety."
                "".format(meta, key)
            )
        if isinstance(value, float) or isinstance(value, Decimal):
            # decimal_format = "{:."+str(precision)+"f}"
            # pair[1] = decimal_format.format(round(value, precision))
            pair[1] = show_fewest(round(value, precision))
            # pair[1] = show_fewest(value)
        else:
            pair[1] = "{}".format(value)
        return True
    return False


def meta_to_cmd(meta):
    '''
    Transform a list of key-value pairs (2-long tuples or lists) into a
    single g-code command string.
    '''
    result = ""
    prefix = ""
    for pair in meta:
        result += prefix
        if len(pair) != 2:
            raise ValueError(
                "Each list in meta from get_cmd_meta should be a pair,"
                " but there is a different number of parts in: {}"
                "".format(pair)
            )
        for part in pair:
            result += "{}".format(part)
        prefix = " "
    return result


def changed_cmd(cmd, key, value, precision=5):
    '''
    Parse the g-code command and after key, change the number to value.
    If value is a float or decimal, format it to the number of places
    specified by precision.
    Otherwise, format it directly (assume it is a string with the
    correct number of decimal places or an int that should have no
    decimal places).
    '''
    meta = get_cmd_meta(cmd)
    result = modify_cmd_meta(meta, key, value, precision=precision)
    if not result:
        return cmd
    return meta_to_cmd(meta)


def get_cmd_meta(cmd):
    '''
    Parse the g-code command to a set of lists such as:
    [['G', '1'], ['X', '110'], ['E', '45'], ['F', '500.0']]
    [['M', '117'], ['', 'Some message']]
    '''
    comment_i = None
    '''
    commentMarks = [";", "//"]
    for commentMark in commentMarks:
      tryI = cmd.find(commentMark)
      if tryI >= 0:
          if (comment_i is None) or (tryI < comment_i):
              comment_i = tryI
    '''
    tryI = cmd.find(";")
    if tryI >= 0:
        # if (comment_i is None) or (tryI < comment_i):
        comment_i = tryI
    if cmd.strip().startswith("/"):
        # ^ as per <https://www.cnccookbook.com/
        #   g-code-basics-program-format-structure-blocks/>
        # (also takes care of non-standard // comments)
        comment_i = cmd.find("/")
    if comment_i is not None:
        cmd = cmd[0:comment_i]

    cmd = cmd.strip()
    # print("cmd={}".format(cmd))
    if len(cmd) < 1:
        return None
    if cmd[0] == ";":
        # comment
        return None
    parts = cmd.split()
    cmd_meta = []
    functionStr = None
    macro = None
    for i in range(len(parts)):
        arg = parts[i]
        if functionStr is None:
            if len(arg) < 1:
                functionStr = ""
            else:
                functionStr = arg
        if macro is not None:
            klipperArgEndIdx = arg.find("=")
            # if klipperArgEndIdx > -1
            assert klipperArgEndIdx > 0
            # NOTE: *include* = as a special flag
            #   so caller knows it is not a G-code
            #   command.
            cmd_meta.append([
                arg[:klipperArgEndIdx+1], # +1 to *keep* '=' as flag
                arg[klipperArgEndIdx+1:]
            ])
        elif not has_numbers(arg):
            # arg.strip() == "TIMELAPSE_TAKE_FRAME":
            # or TIMELAPSE_RENDER, BED_MESH_PROFILE, etc
            assert i == 0, \
                "misplaced macro {} in {}".format(repr(arg), parts)
            print("Warning: allowing literal \"{}\""
                  " (assuming it is a Klipper-style macro)"
                  .format(arg))
            cmd_meta.append([arg,])
            macro = arg
            # fn_strings = parts
            # if len(fn_strings) == 1:
            #     cmd_meta.append(fn_strings+[None])
            # else:
            #     cmd_meta.append(fn_strings)
            # break
        elif len(arg) > 1:
            k, v = arg[0], arg[1:]
            if functionStr == "M117":
                displayStr = " ".join(parts[1:])
                cmd_meta.append([k, v])
                cmd_meta.append(['', displayStr])
                # ^ See M117 in docstring
                break
            try:
                fv = float(v)
            except ValueError as ex:
                logger.warning('WARNING: "{}" is not a number in "{}"'
                               .format(v, cmd))
            cmd_meta.append([k, v])
        else:
            # no value (such as: To home X, nothing is after 'G1 X'):
            cmd_meta.append([arg[0]])
    return cmd_meta


def cmd_meta_dict(cmd_meta):
    '''
    Change results of get_cmd_meta like
    [['G', '1'], ['X', '110'], ['E', '45'], ['F', '500.0']]
    to a dictionary like:
    {'function': 'G1', 'G': '1', 'X': '110', 'E': '45', 'F': '500.0'}
    '''
    if cmd_meta is None:
        return None
    metaD = {}
    for pair in cmd_meta:
        if metaD.get('function') is None:
            if len(pair) != 2:
                logger.warning("WARNING: The G-code command doesn't have"
                               " 2 parts: {} in {}"
                               .format(pair, cmd_meta))
                metaD['function'] = ''  # prevent gathering it again
            if len(pair) == 1:
                # Klipper-style macro
                #   such as TIMELAPSE_TAKE_FRAME
                #   (no number included in command).
                metaD['function'] = pair[0]
            else:
                metaD['function'] = ''.join(pair)
        if len(pair) == 2:
            k, v = pair
        elif len(pair) == 1:
            k, v = pair[0], None
        else:
            k, v = pair[0], pair[1:]
        metaD[k] = v
    return metaD
