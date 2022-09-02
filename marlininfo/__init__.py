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
import shlex
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

if sys.version_info.major < 3:
    input = raw_input

from pycodetool import (
    to_syntax_error,  # (path, lineN, msg, col=None)
    echo_SyntaxWarning,  # (path, lineN, msg, col=None)
    raise_SyntaxError,  # (path, lineN, msg, col=None)
)
from pycodetool.parsing import (
    substring_after,
    find_after,
    get_cdef,
    set_cdef,
    block_uncomment_line,
    COMMENTED_DEF_WARNING,
    find_non_whitespace,
)

verbosity = 0
verbosities = [True, False, 0, 1, 2]

BTT_TFT_URL = "https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware"
LIN_ADVANCE_K_URL = "https://jgmakerforum.com/discussion/259/beta-jgaurora-a5-firmware-1-1-9c"
TFT24_DOC_COMM = ("  // ^ recommended for TFT24 (See <{}>)".format(BTT_TFT_URL))


A3S_DEF_COMMENTS = {  # A list is multiline, while a string goes at the end.
    'TEMP_SENSOR_0': ("// manual calibration of thermistor"
                      " in JGAurora A5 & A3S V1 hotend"),
    'TEMP_SENSOR_BED': ("// measured to be satisfactorily accurate"
                        " on center of bed within +/- 1 degC."),
    'DEFAULT_AXIS_STEPS_PER_UNIT': [
        ("// ^ E-steps calibrated from 80: 200 yields 206, so do:"
         " 0.97087378640776699029 * 100 = 97"),
        ("// - or Set and save (if EEPROM_SETTINGS enabled) with,"
         " respectively: M92 E97; M500"),
    ],
    'Z_MIN_PROBE_REPEATABILITY_TEST': [
        ("// ^ IF has probe, recommended for TFT24 (See <{}>)"
         "".format(BTT_TFT_URL)),
    ],
    'G26_MESH_VALIDATION': [
        "  // ^ recommended for TFT24 (See <{}>)".format(BTT_TFT_URL),
    ],
    'DEFAULT_Kd': ["    // ^ JGAurora A5 & A3S V1 (tuned at 210C)"],
    'DEFAULT_bedKd': [
        "  // ^ JGAurora A3S (tuned at 70C for 8 cycles: M303 EBED S70 C8)",
        "  // #define DEFAULT_bedKp 10.00",
        "  // #define DEFAULT_bedKi .023",
        "  // #define DEFAULT_bedKd 305.4",
        "  // ^ JGAurora A5 (tuned at 70C)",
        "  // A3S V1 differs from A5 due to bed size:",
        "  // #define DEFAULT_bedKp 27.04",
        "  // #define DEFAULT_bedKi 2.26",
        "  // #define DEFAULT_bedKd 80.84",
        "  // ^ JGAurora A3S (tuned at 60C for 10 cycles: M303 EBED S60 C10)",
    ],
    'X_MIN_POS': "// thanks DaHai.",
    'GRID_MAX_POINTS_X': " // 4 suggested by DaHai, https://www.youtube.com/watch?v=CBlADPgQqL0&t=3m0s",
    # ^ spacing differs (multiple uses)
    # ^ GRID_MAX_POINTS_Y is set to GRID_MAX_POINTS_X by default.
}

A3S_ADV_DEF_COMMENTS = {
    'Z_STEPPER_AUTO_ALIGN': [
        ("// ^ IF has probe, recommended for TFT24 (See <{}>)"
         "".format(BTT_TFT_URL)),
    ],
    'LIN_ADVANCE_K': [
        "  // ^ 1.05 for JGAurora A3S according to Cova on",
        "  //   <{}>".format(LIN_ADVANCE_K_URL),
    ],
    'LONG_FILENAME_HOST_SUPPORT': [
        TFT24_DOC_COMM,
    ],
    'AUTO_REPORT_SD_STATUS': [
        TFT24_DOC_COMM,
    ],
    'SDCARD_CONNECTION': [
        "  // ^ ONBOARD recommended for TFT24 (See <{}>)".format(BTT_TFT_URL),
    ],
    'SERIAL_FLOAT_PRECISION': [
        "// ^ 4 recommended for TFT24 (See <{}>)".format(BTT_TFT_URL),
    ],
    'AUTO_REPORT_TEMPERATURES': [
        TFT24_DOC_COMM.strip(),
    ],
    'AUTO_REPORT_POSITION': [
        TFT24_DOC_COMM.strip(),
    ],
    'M115_GEOMETRY_REPORT': [
        TFT24_DOC_COMM,
    ],
    'REPORT_FAN_CHANGE': [
        TFT24_DOC_COMM.strip(),
    ],
    'HOST_ACTION_COMMANDS': [
        TFT24_DOC_COMM.strip(),
    ],
}

R2X_14T_DEF_COMMENTS = {
}
R2X_14T_ADV_DEF_COMMENTS = {
}

MACHINE_DEF_COMMENTS = {
    'A3S': A3S_DEF_COMMENTS,
    'R2X_14T': R2X_14T_DEF_COMMENTS,
}

MACHINE_ADV_DEF_COMMENTS = {
    'A3S': A3S_ADV_DEF_COMMENTS,
    'R2X_14T': R2X_14T_ADV_DEF_COMMENTS,
}

# After ['#pragma once\n', '\n']:
opening_lines = [
    '#define CONFIG_EXAMPLES_DIR "JGAurora/A3S_V1"',
    '',
    '/**',
    ' * JGAurora A3S V1 configuration',
    ' * Authors: Jake Gustafson, Telli Mantelli, Kris Waclawski, Michael Gilardi & Samuel Pinches',
    ' */',
    '',
]


A3S_CONF = {  # include quotes explicitly for strings.
    'STRING_CONFIG_H_AUTHOR': (
        '"(Jake Gustafson, Telli Mantelli, Kris Waclawski,'
        ' Samuel Pinches & Michael Gilardi, 21 Jan 2018)"'
    ), # + " // Who made the changes." comment is preserved by marlininfo
    'MOTHERBOARD': "BOARD_MKS_GEN_L",
    'CUSTOM_MACHINE_NAME': '"JGAurora A3S"',
    'HEATER_0_MAXTEMP': 265,
    'BED_MAXTEMP': 120,
    'PID_EDIT_MENU': "",  # Poikilos
    'PID_AUTOTUNE_MENU': "",  # Poikilos
    'DEFAULT_Kp_LIST': "{  35.30,  35.30 }",
    'DEFAULT_Ki_LIST': "{   4.35,   4.35 }",
    'DEFAULT_Kd_LIST': "{  71.57,  71.57 }",
    'DEFAULT_Kp': "35.30",
    'DEFAULT_Ki': "4.35",
    'DEFAULT_Kd': "71.57",
    'DEFAULT_bedKp': "60.40",
    'DEFAULT_bedKi': "11.52",
    'DEFAULT_bedKd': "79.16",
    'PIDTEMPBED': "",
    'EXTRUDE_MAXLENGTH': 1000,
    'DEFAULT_MAX_ACCELERATION': "{ 1000, 500, 100, 5000 }",
    'DEFAULT_ACCELERATION': "800",
    'DEFAULT_RETRACT_ACCELERATION': "800",
    'DEFAULT_TRAVEL_ACCELERATION': "1000",
    'DEFAULT_XJERK': "8.0",  # req. CLASSIC_JERK not on by default in Marlin 2
    'DEFAULT_YJERK': "3.0",  # req. CLASSIC_JERK not on by default in Marlin 2
    'JUNCTION_DEVIATION_MM': "0.005",
    'Z_MIN_PROBE_REPEATABILITY_TEST': None,
    'PROBING_BED_TEMP': 63,
    'X_BED_SIZE': 205,
    'Y_BED_SIZE': 205,
    'X_MIN_POS': -5,
    'Z_MAX_POS': 205,
    'MESH_BED_LEVELING': None,
    'LEVELING_BED_TEMP': 63,
    'G26_MESH_VALIDATION': None,
    'MESH_TEST_HOTEND_TEMP': 220,
    'MESH_TEST_BED_TEMP': 63,
    'GRID_MAX_POINTS_X': 4,
    # ^ GRID_MAX_POINTS_Y is set to GRID_MAX_POINTS_X by default.
    # TODO: ^ appears in multiple cases including #elif ENABLED(MESH_BED_LEVELING)
    'MESH_G28_REST_ORIGIN': "",  # go to 0 such as for manual leveling
    'LCD_BED_LEVELING': "",
    'LEVEL_BED_CORNERS': "",
    'EEPROM_SETTINGS': "",
    'PREHEAT_1_LABEL': '"PLA+"',  # Poikilos
    'PREHEAT_1_TEMP_HOTEND': 205,  # Poikilos
    'PREHEAT_1_TEMP_BED': 63,  # Poikilos
    'PREHEAT_1_FAN_SPEED': 255,  # Poikilos
    'NOZZLE_PARK_FEATURE': "",  # Poikilos
    'PRINTCOUNTER': "",  # Poikilos
    'SDSUPPORT': "",
    'INDIVIDUAL_AXIS_HOMING_MENU': "",  # Poikilos
    'SPEAKER': "",
    'REPRAP_DISCOUNT_FULL_GRAPHIC_SMART_CONTROLLER': "",
    'TEMP_SENSOR_BED': 1,

    'TEMP_SENSOR_0': 15,
    'DEFAULT_AXIS_STEPS_PER_UNIT': "{ 80, 80, 800, 100 }",
    # ^ TODO: or "{ 80, 80, 800, 97 }" (100 upstream, 97 Poikilos)
    'DEFAULT_MAX_FEEDRATE': "{ 500, 500, 15, 25 }",
    # ^ default z is 6 which is too slow for first touch of z homing
    'Z_PROBE_FEEDRATE_FAST': "(12*60)",
    # ^ 6*60 is way too slow for first touch of z homing
    'X_MIN_ENDSTOP_INVERTING': "true",
    'Y_MIN_ENDSTOP_INVERTING': "true",
    'Z_MIN_ENDSTOP_INVERTING': "true",
    # Inversions below are flipped vs Marlin 1 recommended upstream
    #   settings (by unofficial JGMaker forum) for some reason:
    'INVERT_X_DIR': "false",
    'INVERT_Y_DIR': "true",
    'INVERT_Z_DIR': "true",
    'INVERT_E0_DIR': "false",
    'HOMING_FEEDRATE_MM_M': "{ (80*60), (80*60), (12*60) }",
    # ^ default 6*60 is way too slow for non-print z moves
    'ENCODER_PULSES_PER_STEP': "5",  # MKS TFT28 V3.0
    'REVERSE_ENCODER_DIRECTION': "",  # MKS TFT28 V3.0
}

A3S_C_A_VALUES = {  # MKS TFT28 V3.0
    'WATCH_BED_TEMP_PERIOD': 90,
    'HOMING_BUMP_DIVISOR': "{ 10, 10, 6 }",
    'QUICK_HOME': "",
    'Z_STEPPER_AUTO_ALIGN': None,
    'Z_STEPPER_ALIGN_ITERATIONS': 3,  # default 5
    'SOUND_MENU_ITEM': "",  # Poikilos (add a mute menu item)
    'LCD_SET_PROGRESS_MANUALLY': "",  # Poikilos (Allow M73 to set %)
    'EVENT_GCODE_SD_ABORT': '"G27"',
    'BABYSTEPPING': "",
    'BABYSTEP_MULTIPLICATOR_Z': 5,
    'BABYSTEP_MULTIPLICATOR_XY': 5,
    'DOUBLECLICK_FOR_Z_BABYSTEPPING': "",
    'LIN_ADVANCE': "",
    'LIN_ADVANCE_K': "1.05",  # see LIN_ADVANCE_K_URL
    'ARC_SUPPORT': "",  # "Disable this feature to save ~3226 bytes"
    # ^ "G2/G3 Arc Support"
    'EMERGENCY_PARSER': "",  # Poikilos


    'LONG_FILENAME_HOST_SUPPORT': None,
    'SDCARD_CONNECTION': None,
    'SERIAL_FLOAT_PRECISION': None,

    # Poikilos:
    'HOST_PROMPT_SUPPORT': "",
    'ADVANCED_PAUSE_FEATURE': "",
    'FILAMENT_CHANGE_UNLOAD_FEEDRATE': "60",
    'FILAMENT_CHANGE_UNLOAD_ACCEL': "25",
    # ^ "(mm/s^2) Lower acceleration may allow a faster feedrate"
    'FILAMENT_CHANGE_UNLOAD_LENGTH': "800",
    'FILAMENT_CHANGE_SLOW_LOAD_FEEDRATE': "8",
    'FILAMENT_CHANGE_SLOW_LOAD_LENGTH': "120",
    'FILAMENT_CHANGE_FAST_LOAD_FEEDRATE': "133",
    'FILAMENT_CHANGE_FAST_LOAD_ACCEL': "25",
    'FILAMENT_CHANGE_FAST_LOAD_LENGTH': "680",
    'PARK_HEAD_ON_PAUSE': "",
    'HOME_BEFORE_FILAMENT_CHANGE': "",
    'FILAMENT_LOAD_UNLOAD_GCODES': "",

}


TFT24_C_VALUES = {
    'G26_MESH_VALIDATION': "",
    'ENCODER_PULSES_PER_STEP': 4,
    'REVERSE_ENCODER_DIRECTION': None,
}

TFT24_C_A_VALUES = {
    'LONG_FILENAME_HOST_SUPPORT': "",
    'AUTO_REPORT_SD_STATUS': "",
    'SDCARD_CONNECTION': "ONBOARD",
    'SERIAL_FLOAT_PRECISION': 4,
    'AUTO_REPORT_TEMPERATURES': "",
    'AUTO_REPORT_POSITION': "",
    'EXTENDED_CAPABILITIES_REPORT': "",  # defined by default
    'M115_GEOMETRY_REPORT': "",  # req. EXTENDED_CAPABILITIES_REPORT
    'REPORT_FAN_CHANGE': "",
    'HOST_ACTION_COMMANDS': "",
}



# TODO: ask for probe and use:

BLTOUCH_C_VALUES = {
    'Z_MIN_PROBE_REPEATABILITY_TEST': "",
}
BLTOUCH_C_A_VALUES = {
    'Z_STEPPER_AUTO_ALIGN': "",  # Recommended by TFT24 if using probe
    'MESH_BED_LEVELING': "",
}

R2X_14T_C_VALUES = {
}

R2X_14T_C_A_VALUES = {
}

MACHINE_CONF = {
    'A3S': A3S_CONF,
    'R2X_14T': R2X_14T_C_VALUES,
}

MACHINE_ADV_CONF = {
    'A3S': A3S_C_A_VALUES,
    'R2X_14T': R2X_14T_C_A_VALUES,
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

    def set_c_cdef(self, name, value, comments=None):
        '''
        This operates on self.c_path. For documentation see set_cdef.
        '''
        return set_cdef(self.c_path, name, value, comments=comments)

    def set_c_a_cdef(self, name, value, comments=None):
        '''
        This operates on self.c_a_path. For documentation see set_cdef.
        '''
        return set_cdef(self.c_a_path, name, value, comments=comments)

    def patch_drivers(self, driver_type):
        '''
        Set every driver in driver_names to driver_type.

        Returns:
        a list of names of drivers (macro symbols) that were patched
        '''
        if self.driver_names is None:
            raise ValueError(
                "You must first set driver_names on the MarlinInfo"
                " instance so that which drivers to patch are known."
            )
        return self.set_c_cdef(self.driver_names, driver_type)


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

        for key, value in MACHINE_CONF['A3S'].items():
            comments = MACHINE_DEF_COMMENTS[machine].get(key)
            thisMarlin.set_c_cdef(key, value, comments=comments)

        for key, value in MACHINE_ADV_CONF['A3S'].items():
            comments = MACHINE_ADV_DEF_COMMENTS[machine].get(key)
            thisMarlin.set_c_a_cdef(key, value, comments=comments)

        tft_ans = input("Use a TFT24 (y/n)? ").lower()
        if tft_ans not in ['y', 'n']:
            raise ValueError("You must choose y/n for yes/no")
        tft_v = ""
        if tft_ans == "y":
            for key, value in TFT24_C_VALUES.items():
                comments = MACHINE_DEF_COMMENTS[machine].get(key)
                thisMarlin.set_c_cdef(key, value, comments=comments)

            for key, value in TFT24_C_A_VALUES.items():
                comments = MACHINE_ADV_DEF_COMMENTS[machine].get(key)
                thisMarlin.set_c_a_cdef(key, value, comments=comments)

        runout = input("Use a filament runout sensor (y/n)? ").lower()
        if runout not in ['y', 'n']:
            raise ValueError("You must choose y/n for yes/no")
        runout_v = ""
        if runout == "n":
            runout_v = None
        thisMarlin.set_c_cdef('FILAMENT_RUNOUT_SENSOR', runout_v)
    else:
        usage()
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
    print("# Get patch (for stock headers) using cache:")
    print(shlex.join([
        "diff",
        "-u",
        srcMarlin.c_path,
        thisMarlin.c_path,
    ]))
    print(shlex.join([
        "diff",
        "-u",
        srcMarlin.c_a_path,
        thisMarlin.c_a_path,
    ]))
    print("# Manually merge the changes to complete the process:")
    print(shlex.join(cmd_parts))
    # See <https://stackoverflow.com/a/3516106/4541104>
    proc = Popen(cmd_parts, shell=False,
                 stdin=None, stdout=None, stderr=None, close_fds=True)
    # close_fds: make parent process' file handles inaccessible to child

    return 0


if __name__ == "__main__":
    sys.exit(main())
