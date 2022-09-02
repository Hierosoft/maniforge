#!/usr/bin/env python3
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
)

verbosity = 0
verbosities = [True, False, 0, 1, 2]


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
        with open(self.c_path, 'r') as ins:
            lines = ins.readlines()
        for name in self.driver_names:
            v, line_n, err = get_cdef(self.c_path, name, lines=lines)
            # COMMENTED_DEF_WARNING is ok (using that line is safe
            #   since the warning indicates there is no non-commented
            #   line with the same name)
            if line_n > -1:
                names.append(name)
                rawL = lines[line_n]
                line = rawL.strip()
                if line.startswith("//"):
                    line = line[2:]
                parts = line.split()
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
            else:
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
    if machine is None:
        if "A3S" in this_marlin_name:
            machine = "A3S"
        elif "R2X_14T" in this_marlin_name:
            machine = "R2X_14T"
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
