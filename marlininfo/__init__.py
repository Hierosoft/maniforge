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
    insert_lines,
)

verbosity = 0
verbosities = [True, False, 0, 1, 2]

A3S_TOP_LINES_FLAG = "#pragma once"
A3S_TOP_LINES = [
    '',
    '#define CONFIG_EXAMPLES_DIR "JGAurora/A3S_V1"',
    '',
    '/**',
    ' * JGAurora A3S V1 configuration',
    (' * Authors: Jake Gustafson, Telli Mantelli, Kris Waclawski,'
     ' Michael Gilardi & Samuel Pinches'),
    ' */',
]

R2X_14T_TOP_LINES_FLAG = "#pragma once"
R2X_14T_TOP_LINES = [
    '',
    '#define CONFIG_EXAMPLES_DIR "R2X_14T"',
    '',
    '/**',
    ' * MakerBot Replicator 2X with BTT SKR V1.4 Turbo, TFT35 and',
    ' * thermistors not thermocouples (The R2X 14T build is documented',
    ' * at <https://github.com/poikilos/r2x_14t>)',
    ' * Authors: Jake Gustafson',
    ' */',
]

TOP_C_LINES = {
    'A3S': {
        A3S_TOP_LINES_FLAG: A3S_TOP_LINES,
    },
    'R2X_14T': {
        R2X_14T_TOP_LINES_FLAG: R2X_14T_TOP_LINES,
    },
}

TOP_C_A_LINES = {  # This is the same as TOP_C_LINES for now.
    'A3S': {
        A3S_TOP_LINES_FLAG: A3S_TOP_LINES,
    },
    'R2X_14T': {
        R2X_14T_TOP_LINES_FLAG: R2X_14T_TOP_LINES,
    },
}

moved_tpu = {
    'PREHEAT_2_LABEL': '"TPU"',
    'PREHEAT_2_TEMP_HOTEND': 210,
    'PREHEAT_2_TEMP_BED': 45,
    'PREHEAT_2_TEMP_CHAMBER': 35,
    'PREHEAT_2_FAN_SPEED': 0,
}

moved_abs = {
    'PREHEAT_3_LABEL': '"ABS"',
    'PREHEAT_3_TEMP_HOTEND': 240,
    'PREHEAT_3_TEMP_BED': 110,
    'PREHEAT_3_TEMP_CHAMBER': 35,
    'PREHEAT_3_FAN_SPEED': 0,
}

tpu = moved_tpu
tpu_lines = [  # These will be overwritten if moved_ dicts above are used.
    '',
    '#define PREHEAT_3_LABEL       {}'.format(tpu['PREHEAT_2_LABEL']),
    '#define PREHEAT_3_TEMP_HOTEND {}'.format(tpu['PREHEAT_2_TEMP_HOTEND']),
    '#define PREHEAT_3_TEMP_BED    {}'.format(tpu['PREHEAT_2_TEMP_BED']),
    '#define PREHEAT_3_TEMP_CHAMBER {}'.format(tpu['PREHEAT_2_TEMP_CHAMBER']),
    '#define PREHEAT_3_FAN_SPEED     {}'.format(tpu['PREHEAT_2_FAN_SPEED']),
]

tpu_lines_flag = "#define PREHEAT_2_FAN_SPEED"

BTT_TFT_URL = "https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware"
LIN_ADVANCE_K_URL = (
    "https://jgmakerforum.com/discussion/259/beta-jgaurora-a5-firmware-1-1-9c"
)
BTT_TFT_DOC_COMM = ("  // ^ recommended for BTT TFT (See <{}>)"
                    "".format(BTT_TFT_URL))


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
        ("// ^ IF has probe, recommended for BTT TFT (See <{}>)"
         "".format(BTT_TFT_URL)),
    ],
    'G26_MESH_VALIDATION': [
        "  // ^ recommended for BTT TFT (See <{}>)".format(BTT_TFT_URL),
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
    'GRID_MAX_POINTS_X': (
        " // 4 suggested by DaHai,"
        " https://www.youtube.com/watch?v=CBlADPgQqL0&t=3m0s"
    ),
    # ^ spacing differs (multiple uses)
    # ^ GRID_MAX_POINTS_Y is set to GRID_MAX_POINTS_X by default.
}

A3S_C_A_COMMENTS = {
    'Z_STEPPER_AUTO_ALIGN': [  # Only for using multiple z steppers
        ("// ^ IF has probe, recommended for BTT TFT (See <{}>);"
         " for 2 Z steppers"
         "".format(BTT_TFT_URL)),
    ],
    'LIN_ADVANCE_K': [
        "  // ^ 1.05 for JGAurora A3S according to Cova on",
        "  //   <{}>".format(LIN_ADVANCE_K_URL),
    ],
}

# Done *before* printer so can be overridden:
POIKILOS_C_VALUES = {  # Add more features. They should usually work.
    'PID_EDIT_MENU': "",
    'PID_AUTOTUNE_MENU': "",
    'PREHEAT_1_LABEL': '"PLA+"',
    'PREHEAT_1_TEMP_HOTEND': 205,
    'PREHEAT_1_TEMP_BED': 63,
    'PREHEAT_1_FAN_SPEED': 0,
    'NOZZLE_PARK_FEATURE': "",
    'PRINTCOUNTER': "",
    'INDIVIDUAL_AXIS_HOMING_MENU': "",
    'PIDTEMPBED': "",
    'PROBING_BED_TEMP': 63,
    # PROBING_NOZZLE_TEMP: See printer-specific values.
    'LEVELING_BED_TEMP': 63,
    'MESH_TEST_HOTEND_TEMP': 220,
    'MESH_TEST_BED_TEMP': 63,
}
POIKILOS_C_A_VALUES = {
    'SOUND_MENU_ITEM': "",  # (add a mute menu item)
    'LCD_SET_PROGRESS_MANUALLY': "",  # (Allow M73 to set %)
    'ARC_SUPPORT': "",  # "Disable this feature to save ~3226 bytes"
    # ^ "G2/G3 Arc Support"
    'EMERGENCY_PARSER': "",
    'LIN_ADVANCE': "",
    'HOST_PROMPT_SUPPORT': "",  # req: HOST_ACTION_COMMANDS
    'ADVANCED_PAUSE_FEATURE': "",
    'FILAMENT_LOAD_UNLOAD_GCODES': "",
    'HOST_PAUSE_M76': "",  # TODO: Verify if useful. req: HOST_ACTION_COMMANDS
    'PARK_HEAD_ON_PAUSE': "",
    'HOME_BEFORE_FILAMENT_CHANGE': "",  # Prevent oozing and melting workpiece
    'LCD_INFO_MENU': "",  # not tried with MKS TFT28 V3.0
    'LCD_TIMEOUT_TO_STATUS': 15000,   # uncomment it only
    'SQUARE_WAVE_STEPPING': "",
    # 'TMC_DEBUG': "",  # This was on. See if it is necessary for anything.
}


# Yeah, there really are no comments. There aren't dups elsewhere.
POIKILOS_C_COMMENTS = {
}
POIKILOS_C_A_COMMENTS = {
}

for key, value in POIKILOS_C_VALUES.items():
    if A3S_DEF_COMMENTS.get(key) is not None:
        raise ValueError(
            '{} is already set in POIKILOS_C_A_VALUES'
            ' so the comment should be there instead of in A3S.'
            ''.format(key)
        )

for key, value in POIKILOS_C_A_VALUES.items():
    if A3S_C_A_COMMENTS.get(key) is not None:
        raise ValueError(
            '{} is already set in POIKILOS_C_A_VALUES'
            ' so the comment should be there instead of in A3S.'
            ''.format(key)
        )

# PID Tuning Guide here: https://reprap.org/wiki/PID_Tuning
# ^ The comment is still also in Configuration.h though it moved.

OLD_TO_NEW = {
    # Changed somewhere between
    # Marlin 2.0.x-bugfix 02000903 to 02000905:
    'LEVEL_BED_CORNERS': 'LCD_BED_TRAMMING',
    'LEVEL_CORNERS_INSET_LFRB': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CORNERS_HEIGHT': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CORNERS_Z_HOP': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CENTER_TOO': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CORNERS_USE_PROBE': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CORNERS_PROBE_TOLERANCE': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CORNERS_VERIFY_RAISED': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CORNERS_AUDIO_FEEDBACK': 'BED_TRAMMING_LEVELING_ORDER',
    'LEVEL_CORNERS_LEVELING_ORDER': 'BED_TRAMMING_LEVELING_ORDER',
    'DWIN_CREALITY_LCD_ENHANCED': 'DWIN_LCD_PROUI',
    'TOOLCHANGE_FS_INIT_BEFORE_SWAP': 'TOOLCHANGE_FS_SLOW_FIRST_PRIME',
    'LASER_POWER_INLINE_TRAPEZOID': 'LASER_POWER_TRAP',
    'LASER_POWER_INLINE': 'LASER_POWER_SYNC',
}

DEPRECATED = {  # These are refactored and there is no one to one conversion.
    # Changed somewhere between
    # Marlin 2.0.x-bugfix 02000903 to 02000905:
    'X_DUAL_STEPPER_DRIVERS': "See DUAL_X_CARRIAGE etc instead.",
    'NUM_Z_STEPPER_DRIVERS': "See Z2_DRIVER_TYPE etc instead.",
    'NOZZLE_PARK_MOVE': "See NOZZLE_PARK_X_ONLY and NOZZLE_PARK_Y_ONLY instead.",
    'Z_STEPPER_ALIGN_KNOWN_STEPPER_POSITIONS': (
        "ifdef Z_STEPPER_ALIGN_STEPPER_XY is checked instead now."
    ),
    'HAS_LCD_MENU': "Merged with HAS_MANUAL_MOVE_MENU",
    'HAS_DWIN_E3V2': "Merged with HAS_MANUAL_MOVE_MENU",
}

DEPRECATED_VALUES = {
    'BLTOUCH_HS_MODE': [""],
    # ^ Changed to true/false (Python boolean or C-like boolean string)
}

A3S_CONF = {  # include quotes explicitly for strings.
    'STRING_CONFIG_H_AUTHOR': (
        '"(Jake Gustafson, Telli Mantelli, Kris Waclawski,'
        ' Samuel Pinches & Michael Gilardi, 2 Sep 2022)"'
    ),  # + " // Who made the changes." comment is preserved by marlininfo
    'MOTHERBOARD': "BOARD_MKS_GEN_L",
    'CUSTOM_MACHINE_NAME': '"JGAurora A3S"',
    'HEATER_0_MAXTEMP': 265,
    'BED_MAXTEMP': 120,
    'DEFAULT_Kp_LIST': "{  35.30,  35.30 }",
    'DEFAULT_Ki_LIST': "{   4.35,   4.35 }",
    'DEFAULT_Kd_LIST': "{  71.57,  71.57 }",
    'DEFAULT_Kp': "35.30",
    'DEFAULT_Ki': "4.35",
    'DEFAULT_Kd': "71.57",
    'DEFAULT_bedKp': "60.40",
    'DEFAULT_bedKi': "11.52",
    'DEFAULT_bedKd': "79.16",
    'EXTRUDE_MAXLENGTH': 1000,
    'DEFAULT_MAX_ACCELERATION': "{ 1000, 500, 100, 5000 }",
    'DEFAULT_ACCELERATION': "800",
    'DEFAULT_RETRACT_ACCELERATION': "800",
    'DEFAULT_TRAVEL_ACCELERATION': "1000",
    'DEFAULT_XJERK': "8.0",  # req. CLASSIC_JERK not on by default in Marlin 2
    'DEFAULT_YJERK': "3.0",  # req. CLASSIC_JERK not on by default in Marlin 2
    'JUNCTION_DEVIATION_MM': "0.005",
    'Z_MIN_PROBE_REPEATABILITY_TEST': None,
    'X_BED_SIZE': 205,
    'Y_BED_SIZE': 205,
    'X_MIN_POS': -5,
    'Z_MAX_POS': 205,
    'MESH_BED_LEVELING': None,
    'G26_MESH_VALIDATION': None,
    'GRID_MAX_POINTS_X': 4,
    # ^ GRID_MAX_POINTS_Y is set to GRID_MAX_POINTS_X by default.
    # TODO: ^ appears in multiple cases including
    #   #elif ENABLED(MESH_BED_LEVELING)
    'MESH_G28_REST_ORIGIN': "",  # go to 0 such as for manual leveling

    'LCD_BED_LEVELING': "",
    'LCD_BED_TRAMMING': "",
    'LEVEL_BED_CORNERS': "",  # renamed to LCD_BED_TRAMMING in later versions.
    'EEPROM_SETTINGS': "",
    'SDSUPPORT': "",
    'SPEAKER': "",  # ok for the included MKS TFT28, or swapped to BTT TFT24 etc
    'REPRAP_DISCOUNT_FULL_GRAPHIC_SMART_CONTROLLER': "",  # MKS TFT28, or BTT
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
    'Z_STEPPER_AUTO_ALIGN': "",  # For 2 Z steppers (rec by BTT TFT for probe)
    'Z_STEPPER_ALIGN_ITERATIONS': 3,  # default 5
    'EVENT_GCODE_SD_ABORT': '"G27"',
    'BABYSTEPPING': "",
    'BABYSTEP_MULTIPLICATOR_Z': 5,
    'BABYSTEP_MULTIPLICATOR_XY': 5,
    'DOUBLECLICK_FOR_Z_BABYSTEPPING': "",
    'LIN_ADVANCE_K': "1.05",  # see LIN_ADVANCE_K_URL

    'LONG_FILENAME_HOST_SUPPORT': None,
    'SDCARD_CONNECTION': None,
    'SERIAL_FLOAT_PRECISION': None,

    # Poikilos A3S-specific values:
    'FILAMENT_CHANGE_UNLOAD_FEEDRATE': "60",
    'FILAMENT_CHANGE_UNLOAD_ACCEL': "25",
    # ^ "(mm/s^2) Lower acceleration may allow a faster feedrate"
    'FILAMENT_CHANGE_UNLOAD_LENGTH': "800",
    'FILAMENT_CHANGE_SLOW_LOAD_FEEDRATE': "8",
    'FILAMENT_CHANGE_SLOW_LOAD_LENGTH': "120",
    'FILAMENT_CHANGE_FAST_LOAD_FEEDRATE': "133",
    'FILAMENT_CHANGE_FAST_LOAD_ACCEL': "25",
    'FILAMENT_CHANGE_FAST_LOAD_LENGTH': "680",
}


# Done *after* POIKILOS_ & MACHINE_ values so overrides stock screen:
BTT_TFT_C_VALUES = {
    # 'G26_MESH_VALIDATION': "",  See BLTouch instead.
    'ENCODER_PULSES_PER_STEP': 4,
    'REVERSE_ENCODER_DIRECTION': None,
    'SPEAKER': "",
    'REPRAP_DISCOUNT_FULL_GRAPHIC_SMART_CONTROLLER': "",
}
BTT_TFT_C_COMMENTS = {
}

BTT_TFT_C_A_VALUES = {
    'LONG_FILENAME_HOST_SUPPORT': "",
    'AUTO_REPORT_SD_STATUS': "",
    'SDCARD_CONNECTION': "ONBOARD",
    'SERIAL_FLOAT_PRECISION': 4,
    'AUTO_REPORT_TEMPERATURES': "",
    'AUTO_REPORT_POSITION': "",
    'EXTENDED_CAPABILITIES_REPORT': "",  # defined by default
    'M115_GEOMETRY_REPORT': "",  # req. EXTENDED_CAPABILITIES_REPORT
    'M114_DETAIL': "",  # TODO: See if this is actually used by anything.
    'REPORT_FAN_CHANGE': "",
    'HOST_ACTION_COMMANDS': "",
    'LONG_FILENAME_HOST_SUPPORT': "",  # TODO: test this on MKS TFT28
    'SCROLL_LONG_FILENAMES': "",  # TODO: test this on MKS TFT28
}
BTT_TFT_C_A_COMMENTS = {
    'LONG_FILENAME_HOST_SUPPORT': [
        BTT_TFT_DOC_COMM,
    ],
    'AUTO_REPORT_SD_STATUS': [
        BTT_TFT_DOC_COMM,
    ],
    'SDCARD_CONNECTION': [
        "  // ^ ONBOARD recommended for BTT TFT (See <{}>)".format(BTT_TFT_URL),
    ],
    'SERIAL_FLOAT_PRECISION': [
        "// ^ 4 recommended for BTT TFT (See <{}>)".format(BTT_TFT_URL),
    ],
    'AUTO_REPORT_TEMPERATURES': [
        BTT_TFT_DOC_COMM.strip(),
    ],
    'AUTO_REPORT_POSITION': [
        BTT_TFT_DOC_COMM.strip(),
    ],
    'M115_GEOMETRY_REPORT': [
        BTT_TFT_DOC_COMM,
    ],
    'REPORT_FAN_CHANGE': [
        BTT_TFT_DOC_COMM.strip(),
    ],
    'HOST_ACTION_COMMANDS': [
        BTT_TFT_DOC_COMM.strip(),
    ],
}

# TODO: On A3S, ask for probe and use BLTOUCH values (See R2X_14T):

BLTOUCH_C_VALUES = {
    'Z_MIN_PROBE_REPEATABILITY_TEST': "",
    'AUTO_BED_LEVELING_BILINEAR': "",
    'G26_MESH_VALIDATION': "",
    'MESH_TEST_HOTEND_TEMP': 220,
    'MESH_TEST_BED_TEMP': 63,
    'USE_ZMIN_PLUG': None,
    'Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN': None,
}
BLTOUCH_C_COMMENTS = {
    'AUTO_BED_LEVELING_BILINEAR': (
        " // specified in the BLTouch Smart V3.1 manual"
    ),
    'USE_ZMIN_PLUG': '// commented out as per BLTouch Smart V3.1 manual',
    'Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN': (
        "  // commented as per the BLTouch Smart V3.1 manual",
    ),
}

BLTOUCH_C_A_VALUES = {
    # 'Z_STEPPER_AUTO_ALIGN': "",  # rec by BTT TFT if probe; for 2 Z steppers
    # ^ See printer-specific overrides that are set BEFORE BLTOUCH values
    'MESH_BED_LEVELING': "",
    'BLTOUCH_DELAY': 500,
    'BLTOUCH_FORCE_SW_MODE': "",
    'PROBE_OFFSET_WIZARD': "",
    'PROBE_OFFSET_WIZARD_START_Z': -4.0,
    'PROBE_OFFSET_WIZARD_XY_POS': "{ X_CENTER, Y_CENTER }",  # uncomment it only
}
BLTOUCH_C_A_COMMENTS = {
    'PROBE_OFFSET_WIZARD_XY_POS': [
        ("      // ^ Set x to halfway (-35) between E0 and probe (-70)"
         " so they straddle the center"),
    ],
}

R2X_14T_C_VALUES = {
    'STRING_CONFIG_H_AUTHOR': (
        '"(Jake Gustafson, BTT SKR V1.4 Turbo + TFT35'
        ' for Replicator 2X but with thermistors)"'
    ),  # + " // Who made the changes." comment is preserved by marlininfo
    'CUSTOM_MACHINE_NAME': '"R2X 14T"',
    'BAUDRATE': 115200,
    'SERIAL_PORT_2': -1,
    'MOTHERBOARD': "BOARD_BTT_SKR_V1_4_TURBO",
    'EXTRUDERS': 2,  # TODO: allow disabling the second extruder
    'HOTEND_OFFSET_X': "{ 0.0, 34.00 }",  # assumes EXTRUDERS is 2
    'HOTEND_OFFSET_Y': "{ 0.0, 0.00 }",  # assumes EXTRUDERS is 2
    'HOTEND_OFFSET_Z': "{ 0.0, -0.00 }",  # assumes EXTRUDERS is 2
    'TEMP_SENSOR_0': 11,
    'TEMP_SENSOR_1': 11,
    'TEMP_SENSOR_BED': 11,
    'TEMP_BED_WINDOW': 3,
    'TEMP_BED_HYSTERESIS': 8,
    'HEATER_0_MAXTEMP': 280,
    'HEATER_1_MAXTEMP': 280,
    'BED_MAXTEMP': 130,
    'PID_PARAMS_PER_HOTEND': None,
    'DEFAULT_Kp': 32.1974,
    'DEFAULT_Ki': 3.7686,
    'DEFAULT_Kd': 68.7697,
    'DEFAULT_bedKp': 33.3357,
    'DEFAULT_bedKi': 4.0417,
    'DEFAULT_bedKd': 68.7382,
    'USE_XMIN_PLUG': None,
    'USE_YMIN_PLUG': None,
    'USE_XMAX_PLUG': "",
    'USE_YMAX_PLUG': "",
    'ENDSTOPPULLUP_ZMIN_PROBE': "",
    'X_MIN_ENDSTOP_INVERTING': True,
    'Y_MIN_ENDSTOP_INVERTING': True,
    'Z_MIN_ENDSTOP_INVERTING': True,
    'X_MAX_ENDSTOP_INVERTING': True,
    'Y_MAX_ENDSTOP_INVERTING': True,
    'Z_MAX_ENDSTOP_INVERTING': True,
    'DISTINCT_E_FACTORS': "",
    'DEFAULT_AXIS_STEPS_PER_UNIT': (
        "{ 88.888889, 88.888889, 400, 91.46125, 91.46125 }"
    ),  # 5 entries assumes EXTRUDERS is 2
    'DEFAULT_MAX_FEEDRATE': "{ 200, 200, 5, 25, 25 }",  # assumes EXTRUDERS is 2
    'DEFAULT_MAX_ACCELERATION': "{ 2000, 2000, 200, 10000, 10000 }",
    # ^ 5 entries assumes EXTRUDERS is 2
    'DEFAULT_ACCELERATION': 2000,
    'DEFAULT_RETRACT_ACCELERATION': 2000,
    'DEFAULT_TRAVEL_ACCELERATION': 2000,
    'DEFAULT_EJERK': 3.5,
    'S_CURVE_ACCELERATION': "",
    'USE_PROBE_FOR_Z_HOMING': "",
    'Z_MIN_PROBE_PIN': None,  # See comment regarding BTT SKR V1.4 *
    'BLTOUCH': "",
    'NOZZLE_TO_PROBE_OFFSET': "{ -36, 0, 0 }",  # TODO: test on FlexionHT
    'PROBING_MARGIN': 24,
    'Z_PROBE_FEEDRATE_FAST': "(4*60)",
    'Z_PROBE_FEEDRATE_SLOW': "(Z_PROBE_FEEDRATE_FAST / 5)",  # default= ... / 2
    'MULTIPLE_PROBING': 2,
    'EXTRA_PROBING': 1,
    'Z_CLEARANCE_DEPLOY_PROBE': 15,
    'Z_CLEARANCE_MULTI_PROBE': 2,
    'Z_MIN_PROBE_REPEATABILITY_TEST': "",
    'PROBING_HEATERS_OFF': "",  # Off prevents interference (induction).
    'PROBING_FANS_OFF': "",
    'PREHEAT_BEFORE_PROBING': "",
    'PROBING_NOZZLE_TEMP': 150,
    'INVERT_X_DIR': True,
    'INVERT_Z_DIR': True,
    'INVERT_E1_DIR': True,
    'X_HOME_DIR': 1,
    'Y_HOME_DIR': 1,
    'X_BED_SIZE': 236,
    'Y_BED_SIZE': 129,  # TODO: See if bigger/smaller with FlexionHT vs custom
    'Z_MAX_POS': 150,
    'LEVELING_NOZZLE_TEMP': 150,  # if PREHEAT_BEFORE_LEVELING
    'LEVELING_BED_TEMP': 63,  # if PREHEAT_BEFORE_LEVELING
    'GRID_MAX_POINTS_X': 5,
    # ^ GRID_MAX_POINTS_Y is set to GRID_MAX_POINTS_X by default.
    'EXTRAPOLATE_BEYOND_GRID': "",
    'LCD_BED_LEVELING': "",
    'LCD_BED_TRAMMING': None,
    'LEVEL_BED_CORNERS': None,  # renamed to LCD_BED_TRAMMING in later versions.
    'Z_SAFE_HOMING': "",
    'EEPROM_SETTINGS': "",
    'SDSUPPORT': "",
    # 'NEOPIXEL_PIN': "",  # Not tried, but may be a way to rig builtin ones
}

R2X_14T_C_A_VALUES = {
    'Z_STEPPER_AUTO_ALIGN': None,  # rec by BTT TFT if probe; for 2 Z steppers
    'THERMAL_PROTECTION_HYSTERESIS': 8,
    'WATCH_TEMP_PERIOD': 25,
    'WATCH_TEMP_INCREASE': 7,
    # 'THERMAL_PROTECTION_BED_PERIOD': 20,  # default is 20
    'THERMAL_PROTECTION_BED_HYSTERESIS': 8,
    'WATCH_BED_TEMP_INCREASE': 4,
    'HOTEND_IDLE_TIMEOUT': "",
    'HOTEND_IDLE_TIMEOUT_SEC': "(15*60)",
    'HOTEND_IDLE_MIN_TRIGGER': 140,
    'HOTEND_IDLE_NOZZLE_TARGET': 100,
    'HOTEND_IDLE_BED_TARGET': 43,
    'MULTI_NOZZLE_DUPLICATION': "",
    'ADAPTIVE_STEP_SMOOTHING': "",
    'BABYSTEPPING': "",
    'DOUBLECLICK_FOR_Z_BABYSTEPPING': "",
    'BABYSTEP_ZPROBE_OFFSET': "",
}

# TODO: implement per-machine comments.
R2X_14T_C_COMMENTS = {
    'CUSTOM_MACHINE_NAME': [
        '// max length BTT TFT24:        "                     "'
    ],
    'TEMP_SENSOR_1': '// 2ND NOZZLE',
    'DEFAULT_Kd': [
        ('    // ^ FlexionHT, FilaPrint, thermistors not thermocouples,'
         ' r2x_14t part fan duct 1.0,'),
        '    //   7 cycles, 230 C, T0 (left):',
    ],
    'DEFAULT_bedKd': [
        '  // ^ 105 C, enclosed, cold start (30 C):',
        '  // #define DEFAULT_bedKp 56.49',
        '  // #define DEFAULT_bedKi 2.49',
        '  // #define DEFAULT_bedKd 853.97',
        '  // ^ 60 C, not enclosed:',
    ],
    'DEFAULT_AXIS_STEPS_PER_UNIT': [
        '// Extrusion:',
        ('// - Used factory setting 96.275 then calibrated it'
         ' (it extruded 95/100 mm, so result is 91.46125)'),
        '// Movement:',
        ('// > The Replicator 2 and 2x use 18 tooth GT2 pulleys,'
         ' 1/16 microstepping, and 200 steps/rev steppers.'
         ' That makes the proper steps/mm value 88.888889.'),
        ('// > Note that Makerbot used ~88.56 steps/mm in their defaults,'
         ' which is the value you get if you calculate from the belt+pulley'
         ' pitch diameter from the Gates GT2 specs. But this is the value'
         ' you use for calculating belt length required in a closed loop,'
         ' not for steps/mm. The 88.88... number is more accurate.'),
        "// > by Ryan Carlyle Mar 2 '16 at 20:15",
        ("// > - Hey once again, what about z axis then?"
         " – Anton Osadchy Mar 7 '16 at 17:47"),
        ("// > - Z is 400 steps/mm. (8mm lead, 1/16 microstepping,"
         " 200 steps/mm motor.) Sidenote, make sure you don't over-drive"
         " the Z stepper with plug-in drivers, it's only rated to about 0.4A."
         " – Ryan Carlyle Mar 7 '16 at 19:15"),
        ("// > - @RyanCarlyle FYI minor typo above, you say 200 steps/mm"
         " for Z but I think you mean steps/rev since you already state"
         " Z is 400 steps/mm. Thank you for accurate numbers though!"
         " – guru_florida Aug 22 '20 at 15:12"),
        '//',
        '// -<https://3dprinting.stackexchange.com/a/678>',
    ],
    'Z_MIN_PROBE_PIN': [
        ("// ^ already defined as P0_10 in"
         " Marlin\\src\\pins\\lpc1768\\pins_BTT_SKR_V1_4.h"),
        ("//   (and Marlin\\src\\pins\\lpc1769\\pins\\BTT_SKR_V1_4_TURBO.h"
         " includes it)."),
    ],
    'NOZZLE_TO_PROBE_OFFSET': (
        "// This was set for a hand-machined cooling block"
        " (z=+3.65 when not deployed; 6.07 using dial and 0.1mm feeler gauge),"
        " but may be or may need to be updated for FlexionHT"
    ),
    'Z_PROBE_FEEDRATE_FAST': [
        "// This Poikilos setting (4*60 based on HOMING_FEEDRATE_MM_M",
        "//   --The old setting was formerly HOMING_FEEDRATE_Z)",
        "//   became the new default coincidentally (The default changed",
        "//   somewhere between CONFIGURATION_H_VERSION 020008 and 02000901)",
    ],
    'HOTEND_OFFSET_X': " // (mm) relative X-offset for each nozzle",
    'HOTEND_OFFSET_Y': " // (mm) relative Y-offset for each nozzle",
    'HOTEND_OFFSET_Z': " // (mm) relative Z-offset for each nozzle",
}

R2X_14T_C_A_COMMENTS = {
    'WATCH_BED_TEMP_INCREASE': [
        ("  // ^ Based on approximate stopwatch readings,"
         " the Replicator 2X bed heats"),
        "  //   at 1C per 8s to up to about 27s at first!",
        "  //   When the bed first starts heating, it is very slow,",
        "  //   even if you reset it and start around 35C.",
    ],
}


MACHINE_DEF_COMMENTS = {
    'A3S': A3S_DEF_COMMENTS,
    'R2X_14T': R2X_14T_C_COMMENTS,
}

MACHINE_ADV_DEF_COMMENTS = {
    'A3S': A3S_C_A_COMMENTS,
    'R2X_14T': R2X_14T_C_A_COMMENTS,
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

    def insert_c(self, new_lines, lines=None, after=None):
        '''
        Insert into self.c_path (or lines if present).
        For documentation see insert_lines.
        '''
        return insert_lines(self.c_path, new_lines, lines=lines, after=after)

    def insert_c_a(self, new_lines, lines=None, after=None):
        '''
        Insert into self.c_a_path (or lines if present).
        For documentation see insert_lines.
        '''
        return insert_lines(self.c_a_path, new_lines, lines=lines, after=after)

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
        echo0("Error: The configuration versions are incompatible. First try:")
        echo0('  meld "{}" "{}"'.format(srcMarlin.mm_path, dstMarlin.mm_path))
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
    if machine is None:
        # See also `else` under machine cases.
        usage()
        raise ValueError(
            'A3S or R2X_14T is not in "{}"'
            ' so the machine could not be detected.'
            ' Try setting --machine <machine>.'
            ''.format(this_marlin_name)
        )
    print('machine={}'.format(machine))

    # Add TPU to the preheat menu:
    thisMarlin.insert_c(tpu_lines, after=tpu_lines_flag)
    for key, value in moved_abs.items():
        # Overwrite tpu items that are in the third entry temporarily.
        thisMarlin.set_c_cdef(key, value)
        # comments=comments
    for key, value in moved_tpu.items():
        # insert tpu items as the second entry
        thisMarlin.set_c_cdef(key, value)
        # comments=comments

    for key, value in POIKILOS_C_VALUES.items():
        comments = POIKILOS_C_COMMENTS.get(key)
        thisMarlin.set_c_cdef(key, value, comments=comments)

    for key, value in POIKILOS_C_A_VALUES.items():
        comments = POIKILOS_C_A_COMMENTS.get(key)
        thisMarlin.set_c_a_cdef(key, value, comments=comments)

    for key, value in MACHINE_CONF[machine].items():
        comments = MACHINE_DEF_COMMENTS[machine].get(key)
        thisMarlin.set_c_cdef(key, value, comments=comments)

    for key, value in MACHINE_ADV_CONF[machine].items():
        comments = MACHINE_ADV_DEF_COMMENTS[machine].get(key)
        thisMarlin.set_c_a_cdef(key, value, comments=comments)

    insertions = TOP_C_LINES.get(machine)
    for flag, new_lines in insertions.items():
        thisMarlin.insert_c(new_lines, after=flag)

    insertions = TOP_C_A_LINES.get(machine)
    for flag, new_lines in insertions.items():
        thisMarlin.insert_c_a(new_lines, after=flag)

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

        # Always use BTT TFT values for R2X_14T (ok for TFT35 as well):
        for key, value in BTT_TFT_C_VALUES.items():
            comments = BTT_TFT_C_COMMENTS.get(key)
            thisMarlin.set_c_cdef(key, value, comments=comments)
        for key, value in BTT_TFT_C_A_VALUES.items():
            comments = BTT_TFT_C_A_COMMENTS.get(key)
            thisMarlin.set_c_a_cdef(key, value, comments=comments)

        for key, value in BLTOUCH_C_VALUES.items():
            comments = BLTOUCH_C_COMMENTS.get(key)
            thisMarlin.set_c_cdef(key, value, comments=comments)
        for key, value in BLTOUCH_C_A_VALUES.items():
            comments = BLTOUCH_C_A_COMMENTS.get(key)
            thisMarlin.set_c_a_cdef(key, value, comments=comments)
    elif machine == "A3S":
        thisMarlin.driver_names = [
            'X_DRIVER_TYPE',
            'Y_DRIVER_TYPE',
            'Z_DRIVER_TYPE',
            'E0_DRIVER_TYPE',
        ]
        tft_ans = input("Use a BTT TFT (y/n)? ").lower()
        if tft_ans not in ['y', 'n']:
            raise ValueError("You must choose y/n for yes/no")
        tft_v = ""
        if tft_ans == "y":
            for key, value in BTT_TFT_C_VALUES.items():
                comments = BTT_TFT_C_COMMENTS.get(key)
                thisMarlin.set_c_cdef(key, value, comments=comments)

            for key, value in BTT_TFT_C_A_VALUES.items():
                comments = BTT_TFT_C_A_COMMENTS.get(key)
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
        raise NotImplementedError('machine="{}"'.format(machine))
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
