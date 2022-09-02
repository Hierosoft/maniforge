#!/usr/bin/env python3
'''
marlininfo
----------
by Poikilos

Modify the Marlin configuration in a predictable way regardless of the
configuration version. Copy, modify, then deploy a source Marlin
configuration in the current working directory to a specified copy of
the Marlin sourcecode.

Running main only can work for R2X_14T or JGAurora A3S. If you need to
utilize the framework yourself, you will have to set the driver_names
(list attribute) manually on any MarlinInfo instance you create.

For instructions on compiling Marlin 2 and flashing it to JGAurora A3S,
see ../documentation/A3S_V1.md.

OPTIONS:
--machine <name>        Set the machine name to R2X_14T or A3S for some
                        automatic settings such as what drivers are
                        installed on the board. If the current working
                        directory contains either of those two strings,
                        this setting will be determined automatically.

--driver-type           For each driver installed on the board
                        (as defined by the driver_names list),
                        set the driver type in Configuration.h to
                        this value. This setting will be auto-detected
                        when possible based on value of the "machine".

--help                  Show this help screen.

'''
from __future__ import print_function
import os
import sys
import pathlib
import shutil
from subprocess import (
    Popen,
)

MODULE_DIR = os.path.dirname(__file__)
REPO_DIR = os.path.dirname(MODULE_DIR)
REPOS_DIR = os.path.dirname(REPO_DIR)

CACHES_DIR = os.path.join(pathlib.Path.home(), ".cache")
MY_CACHE_DIR = os.path.join(CACHES_DIR, "marlininfo")

for try_repos_dir in [REPO_DIR, REPOS_DIR]:
    try_repo = os.path.join(try_repos_dir, "pycodetool")
    if os.path.isfile(os.path.join(try_repo, "pycodetool", "__init__.py")):
        sys.path.insert(0, try_repo)
        break


from pycodetool import (
    to_syntax_error,  # (path, lineN, msg, col=None)
    echo_SyntaxWarning,  # (path, lineN, msg, col=None)
    raise_SyntaxError,  # (path, lineN, msg, col=None)
)
from pycodetool.parsing import (
    substring_after,
    find_after,
    get_cdef,
    block_uncomment_line,
    COMMENTED_DEF_WARNING,
    find_non_whitespace,
)

verbosity = 0
verbosities = [True, False, 0, 1, 2]


A3S_DEF_COMMENTS = {
    'DEFAULT_AXIS_STEPS_PER_UNIT': [
        "// E-steps calibrated from 80: 200 yields 206, so do: 0.97087378640776699029 * 100 = 97",
        "// - or Set and save (if EEPROM_SETTINGS enabled) with, respectively: M92 E97; M500",
    ],
    'Z_MIN_PROBE_REPEATABILITY_TEST': [
        "// ^ IF has probe, recommended for TFT24 (See <https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware>)",
    ],
    'G26_MESH_VALIDATION': [
        "// ^ recommended for TFT24 (See <https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware>)",
    ],
}

R2X_14T_DEF_COMMENTS = {
}

MACHINE_DEF_COMMENTS = {
    'A3S': A3S_DEF_COMMENTS,
    'R2X_14T': R2X_14T_DEF_COMMENTS,
}


def set_verbosity(level):
    global verbosity
    if level not in verbosities:
        raise ValueError("level must be one of {}".format(verbosities))
    verbosity = level


def echo0(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)
    return True


def echo1(*args, **kwargs):
    if verbosity < 1:
        return False
    print(*args, file=sys.stderr, **kwargs)
    return True


def echo2(*args, **kwargs):
    if verbosity < 2:
        return False
    print(*args, file=sys.stderr, **kwargs)
    return True


def usage():
    print(__doc__)


class MarlinInfo:
    '''

    Public attributes:
    mm_path -- The Marlin/Marlin directory containing Configuration*.h.
    m_path -- The Marlin repo directory (or a directory of any other)
        structure containing the "Marlin" directory.
    '''

    TRANSFER_RELPATHS = [
        os.path.join("Marlin", "Configuration.h"),
        os.path.join("Marlin", "Configuration_adv.h"),
    ]

    DRIVER_NAMES = [
        'X_DRIVER_TYPE',
        'Y_DRIVER_TYPE',
        'Z_DRIVER_TYPE',
        'X2_DRIVER_TYPE',
        'Y2_DRIVER_TYPE',
        'Z2_DRIVER_TYPE',
    ]
    for n in range(3, 5):
        # Z3 to Z4
        DRIVER_NAMES.append('Z{}_DRIVER_TYPE'.format(n))

    DRIVER_NAMES += [
        'I_DRIVER_TYPE',
        'J_DRIVER_TYPE',
        'K_DRIVER_TYPE',
    ]

    for n in range(8):
        # E0 to E7
        DRIVER_NAMES.append('E{}_DRIVER_TYPE'.format(n))

    def __init__(self, path):
        sub = os.path.split(path)[1]
        MarlinMarlin = os.path.join(path, "Marlin")
        c_rel = os.path.join("Marlin", "Configuration.h")
        c_a_rel = os.path.join("Marlin", "Configuration_adv.h")
        self.c_path = os.path.join(path, c_rel)
        self.c_a_path = os.path.join(path, c_a_rel)
        self.driver_names = None

        if not os.path.isdir(MarlinMarlin):
            # Check if we are in MarlinMarlin already:
            try_c_path = os.path.join(os.path.dirname(path), "Configuration.h")
            try_c_a_path = os.path.join(os.path.dirname(path),
                                        "Configuration_adv.h")
            if not os.path.isfile(try_c_path):
                raise FileNotFoundError(
                    'Error: "{}" does not exist (also tried "{}")'
                    ''.format(self.c_path, try_c_path)
                )
                return 1
            if not os.path.isfile(try_c_a_path):
                raise FileNotFoundError(
                    'Error: "{}" does not exist (also tried "{}")'
                    ''.format(self.c_a_path, try_c_a_path)
                )
                return 1
            self.c_path = try_c_path
            self.c_a_path = try_c_a_path
        if not os.path.isfile(self.c_path):
            raise FileNotFoundError(
                'Error: "{}" does not exist (also tried "{}")'
                ''.format(self.c_path)
            )
            return 1
        if not os.path.isfile(self.c_path):
            raise FileNotFoundError(
                'Error: "{}" does not exist (also tried "{}")'
                ''.format(self.c_a_path)
            )
            return 1
        self.mm_path = os.path.dirname(self.c_path)
        self.m_path = os.path.dirname(self.mm_path)


    def get_c_cdef(self, name):
        '''
        Get a a 3-long tuple with the value of the named #define from
        Marlin/Configuration.h along with the line number and error
        if any.
        '''
        return get_cdef(self.c_path, name)

    def get_c_a_cdef(self, name):
        '''
        Get a a 3-long tuple with the value of the named #define from
        Marlin/Configuration_adv.h along with the line number and error
        if any.
        '''
        return get_cdef(self.c_a_path, name)

    def get_confs_versions(self):
        '''
        Get a tuple of the values CONFIGURATION_H_VERSION and
        CONFIGURATION_ADV_H_VERSION as strings.
        '''
        return (
            self.get_c_cdef("CONFIGURATION_H_VERSION")[0],
            self.get_c_a_cdef("CONFIGURATION_ADV_H_VERSION")[0],
        )

    def copy_to(self, repo_path):
        '''
        Copy configs from mm_path to os.path.join(repo_path, "Marlin")
        --the Marlin/Marlin subdirectory will be created if it doesn't
        exist, where Marlin/ is repo_path.
        '''
        if not os.path.isdir(repo_path):
            raise FileNotFoundError('"{}" does not exist.'.format(repo_path))
        dest_mm_path = os.path.join(repo_path, "Marlin")
        if not os.path.isdir(dest_mm_path):
            os.mkdir(dest_mm_path)
        for src in MarlinInfo.TRANSFER_RELPATHS:
            srcPath = os.path.join(self.m_path, src)
            dstPath = os.path.join(repo_path, src)
            shutil.copy(srcPath, dstPath)

    def drivers_dict(self):
        results = {}
        for name in MarlinInfo.DRIVER_NAMES:
            v, line_n, err = self.get_c_cdef(name)
            if err == COMMENTED_DEF_WARNING:
                continue
            elif v is not None:
                results[name] = v
        return results


    def patch_drivers(self, driver_type):
        '''
        Returns:
        a list of names of drivers (macro symbols) that were patched
        '''
        if self.driver_names is None:
            raise ValueError(
                "You must first set driver_names on the MarlinInfo"
                " instance so that which drivers to patch are known."
            )
        names = []
        path = self.c_path
        with open(path, 'r') as ins:
            lines = ins.readlines()
        for name in self.driver_names:
            v, line_n, err = get_cdef(path, name, lines=lines)
            line_i = line_n - 1
            # COMMENTED_DEF_WARNING is ok (using that line is safe
            #   since the warning indicates there is no non-commented
            #   line with the same name)
            if line_n > -1:
                names.append(name)
                rawL = lines[line_i]
                line = rawL.strip()
                original_line = line
                if line.startswith("//"):
                    line = line[2:].strip()
                parts = line.split()
                if parts[0] != "#define":
                    raise RuntimeError('{}:{}: expected #define'
                                       ''.format(path, line_n))
                original_v_i = line.find(v)
                after_v_i = original_v_i + len(v)
                '''
                Normally don't use after_v_i directly, because the
                value may have spaces (may be a macro rather than a
                constant), but in this case it is OK since the value v
                is reliable (found by get_cdef) so skip:
                macro_ender = find_non_whitespace(line, comment_i-1, step=-1)
                space_and_comment_i = macro_ender + 1
                comment_i = line.find("//", after_v_i)
                if comment_i < -1:
                    comment_i = len(line)
                original_n = parts[1]
                original_v = parts[2]
                original_v_i = line.find(original_v)
                after_v_i = original_v_i + len(original_v)
                '''
                line = line[:original_v_i] + driver_type + line[after_v_i:]
                lines[line_i] = line
                if line != original_line:
                    echo0("* changed {} to {}".format(v, driver_type))
                    echo0('  * changed "{}" to "{}"'.format(original_line, line))

        with open(self.c_path, 'w') as outs:
            for rawL in lines:
                if not rawL.endswith("\n"):
                    rawL += "\n"
                outs.write(rawL)

        return names


def main():
    try:
        srcMarlin = MarlinInfo(os.getcwd())
    except FileNotFoundError as ex:
        echo0(str(ex))
        echo0("You must run this from a Marlin repo"
              " (or Marlin/Marlin directory).")
        return 1
    dst_repo_path = None
    options = {}
    key = None
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if key is not None:
            options[key] = arg
            key = None
        elif arg.startswith("--"):
            if arg == "--verbose":
                set_verbosity(1)
            elif arg == "--debug":
                set_verbosity(2)
            elif arg == "--machine":
                key = "machine"
            elif arg == "--driver-type":
                key = "driver-type"
            elif arg in ["--help", "/?"]:
                usage()
                return 0
            else:
                usage()
                echo0("The argument is incorrect: {}".format(arg))
                return 1
        else:
            if dst_repo_path is None:
                dst_repo_path = arg
    if dst_repo_path is None:
        sys.stderr.write(
            "Error: You must specify a destination Marlin directory"
        )
        try_dst = os.path.join(pathlib.Path.home(), "Downloads", "git",
                               "MarlinFirmware", "Marlin")
        if os.path.isdir(try_dst):
            sys.stderr.write(
                ' such as via:\n  {} "{}"\n'.format(sys.argv[0], try_dst)
            )
        else:
            sys.stderr.write(".\n")
        sys.stderr.flush()
        return 1
    dstMarlin = MarlinInfo(dst_repo_path)
    echo0('dst_repo_path="{}"'.format(dst_repo_path))
    echo0('source Configuration.h, _adv versions: {}'
          ''.format(srcMarlin.get_confs_versions()))
    echo0('destination Configuration.h, _adv versions: {}'
          ''.format(dstMarlin.get_confs_versions()))
    if dstMarlin.get_confs_versions() != srcMarlin.get_confs_versions():
        echo0("Error: The configuration versions are incompatible.")
        return 1
    this_marlin_name = os.path.split(srcMarlin.m_path)[1]
    this_data_path = os.path.join(MY_CACHE_DIR, "tmp", this_marlin_name)
    if not os.path.isdir(this_data_path):
        os.makedirs(this_data_path)
    srcMarlin.copy_to(this_data_path)
    thisMarlin = MarlinInfo(this_data_path)

    driver_types = ["A4988", "TMC2209"]
    driver_type = options.get('driver-type')

    machine = options.get('machine')

    if "A3S" in this_marlin_name:
        if machine is None:
            machine = "A3S"
        else:
            echo0('Warning: You set machine to {},'
                  ' but the directory contained the string "A3S"'
                  ''.format(machine))
    elif "R2X_14T" in this_marlin_name:
        if machine is None:
            machine = "R2X_14T"
        else:
            echo0('Warning: You set machine to {},'
                  ' but the directory contained the string "R2X_14T"'
                  ''.format(machine))
    print('machine={}'.format(machine))
    if machine == "R2X_14T":
        driver_types = ["TMC2209"]
        if driver_type is not None:
            if driver_type not in driver_types:
                raise ValueError(
                    "For {} the driver_type {}"
                    " should instead be one of: {}"
                    "".format(machine, driver_type, driver_types)
                )
        else:
            driver_type = driver_types[0]
            print("# automatically selected for {}:".format(machine))
            print("--driver-type {}".format(driver_type))
        thisMarlin.driver_names = [
            'X_DRIVER_TYPE',
            'Y_DRIVER_TYPE',
            'Z_DRIVER_TYPE',
            'E0_DRIVER_TYPE',
            'E1_DRIVER_TYPE',
        ]
    elif machine == "A3S":
        thisMarlin.driver_names = [
            'X_DRIVER_TYPE',
            'Y_DRIVER_TYPE',
            'Z_DRIVER_TYPE',
            'E0_DRIVER_TYPE',
        ]
        '''
        # TODO:
        - 'DEFAULT_AXIS_STEPS_PER_UNIT', "{ 80, 80, 800, 100 }"
          - or "{ 80, 80, 800, 100 }" & use
            MACHINE_DEF_COMMENTS[machine]['DEFAULT_AXIS_STEPS_PER_UNIT']
        - 'DEFAULT_MAX_FEEDRATE', "{ 500, 500, 15, 25 }"
          (default z is 6 which is too slow for first touch of z homing)
        - 'Z_PROBE_FEEDRATE_FAST', "(12*60)"
          (6*60 is way too slow for first touch of z homing)\
        - inversions are all flipped vs Marlin 1 recommended upstream
          settings (by unofficial JGMaker forum) for some reason:
          * 'INVERT_X_DIR', "false"
          * 'INVERT_Y_DIR', "true"
          * 'INVERT_Z_DIR', "true"
          * 'INVERT_E0_DIR', "false"
        - ask user to "remove" (comment) #define FILAMENT_RUNOUT_SENSOR
          (if so, if not commented already, comment it)
        - 'HOMING_FEEDRATE_MM_M', "{ (80*60), (80*60), (12*60) }"
          (default 6*60 is way too slow for non-print z moves)
        - 'ENCODER_PULSES_PER_STEP', "4"
        - comment //#define REVERSE_ENCODER_DIRECTION if not already
        '''
    else:
        raise ValueError(
            'A3S or R2X_14T is not in "{}"'
            ' so the machine could not be detected.'
            ''.format(this_marlin_name)
        )
    default_s = driver_types[0]
    if driver_type is None:
        echo0("Please specify --driver-type such as one of {}"
              "".format(driver_types))
        return 0
    if driver_type is not None:
        drivers_dict = thisMarlin.drivers_dict()
        for this_driver_name, this_driver_type in drivers_dict.items():
            if this_driver_type != driver_type:
                echo0("* changing {} from {} to {}"
                      "".format(this_driver_name, this_driver_type,
                                driver_type))

        thisMarlin.patch_drivers(driver_type)



    cmd_parts = ["meld", thisMarlin.mm_path, dstMarlin.mm_path]
    # See <https://stackoverflow.com/a/3516106/4541104>
    proc = Popen(cmd_parts, shell=False,
             stdin=None, stdout=None, stderr=None, close_fds=True)
    # close_fds: make parent process' file handles inaccessible to child

    return 0


if __name__ == "__main__":
    sys.exit(main())
