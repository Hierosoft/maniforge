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

--T0 <port name>        (default: TH0) Set T0 to TH0 or TH1. TH1 can be
                        used such as when TH0 is damaged, but the number
                        of nozzles will be limited to 1.

--zmax                  (only for R2X_14T; default None) Enable a
                        custom-installed ZMAX endstop (such as if you
                        moved the endstop from the top to the bottom).
                        This is not compatible with
                        Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN (but that
                        setting isn't enabled anywhere in this program
                        for the BTT mainboard).
'''
from __future__ import print_function
import os
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
from pycodetool.parsing import (
    # substring_after,
    # find_after,
    get_cdef,
    # block_uncomment_line,
    COMMENTED_DEF_WARNING,
    # find_non_whitespace,
    # insert_lines,
    # write_lines,
    SourceFileInfo,
    toPythonLiteral,
    cdefs_to_d,
    ECLineInfo,
)

MODULE_DIR = os.path.dirname(__file__)
REPO_DIR = os.path.dirname(MODULE_DIR)
REPOS_DIR = os.path.dirname(REPO_DIR)

CACHES_DIR = os.path.join(pathlib.Path.home(), ".cache")

CONFIGS_DIR = os.path.join(pathlib.Path.home(), ".config")
if platform.system() == "Windows":
    CONFIGS_DIR = os.environ['APPDATA']

MY_CONFIG_DIR = os.path.join(CONFIGS_DIR, "marlininfo")

MY_CACHE_DIR = os.path.join(CACHES_DIR, "marlininfo")

if sys.version_info.major < 3:
    input = raw_input  # noqa: F821

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
    ' * MakerBot Replicator 2X with BTT SKR V1.4 Turbo, TFT35 V3.0 and',
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

MOVED_TPU = {
    'PREHEAT_2_LABEL': '"TPU"',
    'PREHEAT_2_TEMP_HOTEND': 210,
    'PREHEAT_2_TEMP_BED': 30,
    'PREHEAT_2_TEMP_CHAMBER': 35,
    'PREHEAT_2_FAN_SPEED': 0,
}

# TODO: MOVED_TPU_COMMENTS
MOVED_TPU_COMMENTS = {
    'PREHEAT_2_TEMP_HOTEND': " // ~210 for TPU, 170 for ATARAXIA ART Flexible PLA+ or it blobs all over",
    'PREHEAT_2_TEMP_BED': "// ~40 for TPU, 30 for ATARAXIA ART Flexible PLA+ on FilaPrint",
}

MOVED_ABS = {
    'PREHEAT_3_LABEL': '"ABS"',
    'PREHEAT_3_TEMP_HOTEND': 240,
    'PREHEAT_3_TEMP_BED': 110,
    'PREHEAT_3_TEMP_CHAMBER': 35,
    'PREHEAT_3_FAN_SPEED': 0,
}

# TODO: MOVED_ABS_COMMENTS
MOVED_ABS_COMMENTS = {
    'PREHEAT_3_TEMP_HOTEND': " // 240 for FilaPrint, otherwise 245",
    'PREHEAT_3_TEMP_BED': "// 110 for FilaPrint",
}

MOVED_PETG = {
    'PREHEAT_4_LABEL': '"PETG"',
    'PREHEAT_4_TEMP_HOTEND': 250,
    'PREHEAT_4_TEMP_BED': 83,
    'PREHEAT_4_TEMP_CHAMBER': 35,
    'PREHEAT_4_FAN_SPEED': 0,
}

MOVED_PETG_COMMENTS = {
    'PREHEAT_4_TEMP_HOTEND': " // 230 for FilaPrint, otherwise ~250",
    'PREHEAT_4_TEMP_BED': "// 60 for FilaPrint, otherwise 83",
}

tpu = MOVED_TPU
tpu_lines = [  # These will be overwritten if moved_ dicts above are used.
    '',
    '#define PREHEAT_3_LABEL       {}'.format(tpu['PREHEAT_2_LABEL']),
    '#define PREHEAT_3_TEMP_HOTEND {}'.format(tpu['PREHEAT_2_TEMP_HOTEND']),
    '#define PREHEAT_3_TEMP_BED     {}'.format(tpu['PREHEAT_2_TEMP_BED']),
    '#define PREHEAT_3_TEMP_CHAMBER {}'.format(tpu['PREHEAT_2_TEMP_CHAMBER']),
    '#define PREHEAT_3_FAN_SPEED     {}'.format(tpu['PREHEAT_2_FAN_SPEED']),
]

petg = MOVED_PETG
petg_lines = [  # These will be overwritten if moved_ dicts above are used.
    '',
    '#define PREHEAT_4_LABEL       {}'.format(petg['PREHEAT_4_LABEL']),
    '#define PREHEAT_4_TEMP_HOTEND {}'.format(petg['PREHEAT_4_TEMP_HOTEND']),
    '#define PREHEAT_4_TEMP_BED     {}'.format(petg['PREHEAT_4_TEMP_BED']),
    '#define PREHEAT_4_TEMP_CHAMBER {}'.format(petg['PREHEAT_4_TEMP_CHAMBER']),
    '#define PREHEAT_4_FAN_SPEED     {}'.format(petg['PREHEAT_4_FAN_SPEED']),
]

# TODO: AAFPP_LINES
# AAFPP is ATARAXIA ART Flexible PLA+ (behaves like [and probably is] "soft PLA")
AAFPP_LINES = [
    '#define PREHEAT_5_LABEL       "AAFPLA+"',
    '#define PREHEAT_5_TEMP_HOTEND 170 // ~210 for TPU, 170 for ATARAXIA ART Flexible PLA+ or it blobs all over',
    '#define PREHEAT_5_TEMP_BED     30 // ~40 for TPU, 30 for ATARAXIA ART Flexible PLA+ on FilaPrint',
    '#define PREHEAT_5_TEMP_CHAMBER 35',
    '#define PREHEAT_5_FAN_SPEED     0',
]

'''
AAFPP = {
    "PREHEAT_5_LABEL": "AAFPLA+",
    "PREHEAT_5_TEMP_HOTEND": "170",
    "PREHEAT_5_TEMP_BED": "30",
    "PREHEAT_5_TEMP_CHAMBER": "35",
    "PREHEAT_5_FAN_SPEED": "0",
}
'''

AAFPP_COMMENTS = {
    "PREHEAT_5_TEMP_HOTEND": "~210 for TPU, 170 for ATARAXIA ART Flexible PLA+ or it blobs all over",
    "PREHEAT_5_TEMP_BED": "~40 for TPU, 30 for ATARAXIA ART Flexible PLA+ on FilaPrint",
}

tpu_lines_flag = "#define PREHEAT_2_FAN_SPEED"
petg_lines_flag = "#define PREHEAT_3_FAN_SPEED"
AAFPP_lines_flag = "#define PREHEAT_4_FAN_SPEED"
BTT_TFT_URL = "https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware"
ADVANCE_K_URL = (
    "https://jgmakerforum.com/discussion/259/beta-jgaurora-a5-firmware-1-1-9c"
)
BTT_TFT_DOC_COMM = ("  // ^ recommended for BTT TFT (See <{}>)"
                    "".format(BTT_TFT_URL))


A3S_C_COMMENTS = {  # A list is multiline, while a string goes at the end.
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
    'Z_STEPPER_AUTO_ALIGN': [  # Only for using 2 Z *drivers*
        ("// ^ IF has probe, recommended for BTT TFT (See <{}>);"
         " for 2 Z steppers"
         "".format(BTT_TFT_URL)),
    ],
    'ADVANCE_K': [  # formerly LIN_ADVANCE K
        "  // ^ 1.05 for JGAurora A3S according to Cova on",
        "  //   <{}>".format(ADVANCE_K_URL),
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
    'PREHEAT_5_LABEL': '"AAFPLA+"',
    'PREHEAT_5_TEMP_HOTEND': 170,
    'PREHEAT_5_TEMP_BED': 30,
    # 'PREHEAT_5_TEMP_CHAMBER': 35,
    'PREHEAT_5_FAN_SPEED': 0,
    'NOZZLE_PARK_FEATURE': "",
    'PRINTCOUNTER': "",
    'INDIVIDUAL_AXIS_HOMING_MENU': "",
    'PIDTEMPBED': "",
    'PROBING_BED_TEMP': 63,  # See comment!
    # PROBING_NOZZLE_TEMP: See BLTouch (~~or~~ formerly printer)
    'LEVELING_BED_TEMP': 63,
    'MESH_TEST_HOTEND_TEMP': 220,
    'MESH_TEST_BED_TEMP': 63,
    'NOZZLE_CLEAN_FEATURE': "",
    'STARTUP_TUNE': ("{ 698, 300, 0, 50, 523, 50, 0, 25, 494, 50, 0, 25,"
                     " 523, 100, 0, 50, 554, 300, 0, 100, 523, 300 }"),
    # default in bugfix-2.1.x 4c033c3e but disabled
    'EXTRUDE_MAXLENGTH': 201,
}
# TODO: Evaluate whether should be on (off by default, new in Marlin
#   bugfix-2.1.x <= 4c033c3e `//#define Z_SAFE_HOMING_POINT_ABSOLUTE
#   // Ignore home offsets (M206) for Z homing position`

POIKILOS_C_A_VALUES = {
    'SOUND_MENU_ITEM': "",  # (add a mute menu item)
    'SET_PROGRESS_MANUALLY': "",  # Allow M73 to set %
    # ^ formerly 'LCD_SET_PROGRESS_MANUALLY': "",
    'ARC_SUPPORT': "",  # "Disable this feature to save ~3226 bytes"
    # ^ "G2/G3 Arc Support"
    'EMERGENCY_PARSER': "",
    'HOST_PROMPT_SUPPORT': "",  # req: HOST_ACTION_COMMANDS
    'ADVANCED_PAUSE_FEATURE': "",
    'FILAMENT_LOAD_UNLOAD_GCODES': "",
    'HOST_PAUSE_M76': "",  # TODO: Verify if useful. req: HOST_ACTION_COMMANDS
    'PARK_HEAD_ON_PAUSE': "",
    'HOME_BEFORE_FILAMENT_CHANGE': "",  # Prevent oozing and melting workpiece
    'LCD_INFO_MENU': "",  # not tried with MKS TFT28 V3.0
    'LCD_TIMEOUT_TO_STATUS': 15000,   # uncomment it only
    'EDGE_STEPPING': "",  # Formerly SQUARE_WAVE_STEPPING
    # 'TMC_DEBUG': "",  # This was on. See if it is necessary for anything.
}


# Yeah, there really are no comments. There aren't dups elsewhere.
POIKILOS_C_COMMENTS = {
    'PREHEAT_1_TEMP_HOTEND': "205 for FilaPrint",
    'PREHEAT_1_TEMP_BED': "63 for FilaPrint",
    'PREHEAT_2_TEMP_HOTEND': "~210 for TPU, 170 for ATARAXIA ART Flexible PLA+ or it blobs all over ",
    'PREHEAT_2_TEMP_BED': "~40 for TPU, 30 for ATARAXIA ART Flexible PLA+ on FilaPrint ",
    'PREHEAT_3_TEMP_HOTEND': "240 for FilaPrint, otherwise 245",
    'PREHEAT_3_TEMP_BED': "110 for FilaPrint",
    'PREHEAT_4_TEMP_HOTEND': "230 for FilaPrint, otherwise ~250",
    'PREHEAT_4_TEMP_BED': "60 for FilaPrint, otherwise 83",
    'PREHEAT_5_TEMP_HOTEND': "~210 for TPU, 170 for ATARAXIA ART Flexible PLA+ or it blobs all over",
    'PREHEAT_5_TEMP_BED': "~40 for TPU, 30 for ATARAXIA ART Flexible PLA+ on FilaPrint",
    'ENABLE_LEVELING_FADE_HEIGHT': "default enabled is ok (when using probe); Enable fading from mesh level to flat.",
    'DEFAULT_LEVELING_FADE_HEIGHT': "default 10 is ok: change from mesh shape (of bed) to flat over this many mm.",
    'PROBING_BED_TEMP': "Set high since *does* wait for cooling & is after home!",
    'EXTRUDE_MAXLENGTH': "200 is default, but is triggered by webapp based on CNC Kitchen Flow Test which uses 200 exactly (after .8)",
}
POIKILOS_C_A_COMMENTS = {
}

for key, value in POIKILOS_C_VALUES.items():
    if A3S_C_COMMENTS.get(key) is not None:
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
    'NOZZLE_PARK_MOVE': "See NOZZLE_PARK_X_ONLY & NOZZLE_PARK_Y_ONLY instead.",
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
# TODO: ^ is #define COOLER_FAN_PIN -1 from A3S Configuration_adv.h deprecated?

A3S_C_VALUES = {  # include quotes explicitly for strings.
    'STRING_CONFIG_H_AUTHOR': (
        '"(marlininfo by Jake Gustafson, Telli Mantelli, Kris Waclawski,'
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
    'EXTRUDE_MAXLENGTH': 1000,  # Such as for loading
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
    'AUTO_BED_LEVELING_UBL': None,
    'G26_MESH_VALIDATION': None,
    'GRID_MAX_POINTS_X': 4,
    # ^ GRID_MAX_POINTS_Y is set to GRID_MAX_POINTS_X by default.
    # TODO: ^ appears in multiple cases including
    #   #elif ENABLED(MESH_BED_LEVELING)
    'MESH_G28_REST_ORIGIN': "",  # go to 0 such as for manual leveling

    # 'LCD_BED_LEVELING': "",
    'LCD_BED_TRAMMING': "",
    # 'LEVEL_BED_CORNERS': "",  # renamed to LCD_BED_TRAMMING in later versions.
    'EEPROM_SETTINGS': "",
    'SDSUPPORT': "",  # Replaced by HAS_MEDIA (not in Configuration_adv.h)? Back in e41dc27

    'SPEAKER': "",  # tone (instead of beep)
    # 'SPEAKER': "",  # *incompatible now* with mega2560
    # ^ - See [Mega2560 Print Fan
    #     Problem](https://github.com/MarlinFirmware/Marlin/issues/23651)
    # ^ - was ok for the included MKS TFT28 (?), or swapped to BTT TFT24 etc
    # ^ - fixed by FAN_SOFT_PWM (recommended by Marlin compile metadata
    #     and by <https://github.com/MarlinFirmware/Configurations
    #     /tree/bugfix-2.0.x/config/examples/JGAurora/A5>:
    'FAN_SOFT_PWM': "",
    'REPRAP_DISCOUNT_FULL_GRAPHIC_SMART_CONTROLLER': None,  # BTT not MKS TFT28
    'TEMP_SENSOR_BED': 1,

    'TEMP_SENSOR_0': 15,
    'DEFAULT_AXIS_STEPS_PER_UNIT': "{ 80, 80, 800, 94.3396 }",
    # ^ TODO: or "{ 80, 80, 800, 97 }"
    #   (100 upstream, 94.3396 Poikilos (formerly 97))
    'DEFAULT_MAX_FEEDRATE': "{ 500, 500, 15, 25 }",
    # ^ default z is 6 which is too slow for first touch of z homing
    'Z_PROBE_FEEDRATE_FAST': "(12*60)",
    # ^ 6*60 is way too slow for first touch of z homing
    # 'X_MIN_ENDSTOP_INVERTING': True,
    # 'Y_MIN_ENDSTOP_INVERTING': True,
    # 'Z_MIN_ENDSTOP_INVERTING': True,  # later replaced with MAX if moved to MAX!
    # ^ Changed to False if BLTouch
    # ^ Changed in bugfix-2.1.x <= 4c033c3e:
    'X_MAX_ENDSTOP_HIT_STATE': "LOW",
    'Y_MAX_ENDSTOP_HIT_STATE': "LOW",
    'Z_MIN_ENDSTOP_HIT_STATE': "LOW",  # later replaced with MAX if moved to MAX!
    # Inversions below are flipped vs Marlin 1 recommended upstream
    #   settings (by unofficial JGMaker forum) for some reason:
    'INVERT_X_DIR': False,
    'INVERT_Y_DIR': True,
    'INVERT_Z_DIR': True,
    'INVERT_E0_DIR': False,
    'HOMING_FEEDRATE_MM_M': "{ (80*60), (80*60), (12*60) }",
    # ^ default 6*60 is way too slow for non-print z moves
    'ENCODER_PULSES_PER_STEP': None,  # MKS TFT28 V3.0 has no encoder
    'REVERSE_ENCODER_DIRECTION': None,  # MKS TFT28 V3.0 has no encoder
    'NOZZLE_PARK_POINT': "{ (X_MIN_POS + 10), (Y_MAX_POS - 10), 115 }",
}

MATERIALS = {  # formerly K_FACTORS { 'PLA' ... etc
    '3D PrintLife Pro PLA': {
        'brand': "3D PrintLife",
        'material': "PLA",
        'color': "white",
        'K': 0.6,
        'comment': (
            "0.6 for 3D PrintLife Pro PLA retraction 4.8@45 2022-09-02"
            " found using https://marlinfw.org/tools/lin_advance/k-factor.html"
        ),
    },
    'PolyTerra PLA': {
        'brand': "PolyTerra",
        'material': "PLA",
        'color': 'black',
        'K': 0.3325,
        'comment': (
            "0.3325 using LinearAdvanceTowerGenerator (step 0.05)"
        ),
    },
    'FormFutura HDglass': {
        'brand': "FormFutura",
        'material': "PETG",
        'color': "clear",
        'K': 0.8,
        'comment': (
            "0.88 seemed to look better using LinearAdvanceTowerGenerator"
            " but after printing the same tower, 0.8 was better (had no"
            " bulging on corners)"
        ),
    },
}
# Firmware default is set via ADVANCE_K.
# Set later:
# M900  ; report current value (get K)
# M900 K0.56 ; set K
# M500  ; save

# TODO: set K to 0.56: ask user tube inner dia (K1.05 2.0 or 0.56 for 1.9)
# FormFutura HDglass (modified PETG): M900 K0.8 using line test;

#   retraction 4.8 is based on:
#   (1.9 ID - 1.75) / (2.0 stock ID - 1.75) = .6
#   .6 * 8 (Cura default PLA retraction) = 4.8

#
A3S_C_A_VALUES = {  # MKS TFT28 V3.0
    'WATCH_BED_TEMP_PERIOD': 90,
    'HOMING_BUMP_DIVISOR': "{ 10, 10, 6 }",
    'QUICK_HOME': "",
    'Z_STEPPER_AUTO_ALIGN': None,  # For 2 Z *drivers*; rec by BTT TFT for probe
    'Z_STEPPER_ALIGN_ITERATIONS': 3,  # default 5
    'EVENT_GCODE_SD_ABORT': '"G27"',
    'BABYSTEPPING': "",
    'BABYSTEP_MULTIPLICATOR_Z': 5,
    'BABYSTEP_MULTIPLICATOR_XY': 5,
    'DOUBLECLICK_FOR_Z_BABYSTEPPING': "",
    'ADVANCE_K': "1.05",  # see ADVANCE_K_URL. Formerly LIN_ADVANCE_K
    # TODO: ^ Use MATERIALS dict & let the user choose.
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
    'LIN_ADVANCE': "",
}


# Done *after* POIKILOS_ & MACHINE_ values so overrides stock screen:
BTT_TFT_C_VALUES = {
    'BAUDRATE': 115200,
    # 'G26_MESH_VALIDATION': "",  See BLTouch instead.
    'ENCODER_PULSES_PER_STEP': 4,
    'REVERSE_ENCODER_DIRECTION': None,
    # 'SPEAKER': "",  # *incompatible* with mega2560 (See R2X_14T instead)
    'REPRAP_DISCOUNT_FULL_GRAPHIC_SMART_CONTROLLER': "",
}
BTT_TFT_C_COMMENTS = {
}

BTT_TFT_C_A_VALUES = {
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
# TODO: config.ini is used by PlatformIO
# - <https://marlinfw.org/docs/configuration/config-ini.html>
# - *but* Auto Build Marlin is recommended by Marlin
#   - Auto Build Marlin eliminates the need to edit platformio.ini
#     - <https://marlinfw.org/docs/configuration/config-ini.html>
#     - but automatically installs PlatformIO...so do we need to edit
#       H files at all??
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
    'AUTO_REPORT_REAL_POSITION': [
        'TODO: See if this is necessary',
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
    # region moved from R2X_14T and deleted redundant
    'Z_MIN_PROBE_PIN': None,  # See comment regarding BTT SKR V1.4 *
    'USE_PROBE_FOR_Z_HOMING': "",
    'Z_HOME_DIR': "-1",
    'BLTOUCH': "",
    'NOZZLE_TO_PROBE_OFFSET': "{ -35, 0, -2.7737 }",  # See comment
    'PROBING_MARGIN': 24,
    'MULTIPLE_PROBING': 2,
    'EXTRA_PROBING': 1,
    'Z_CLEARANCE_DEPLOY_PROBE': 15,
    'Z_CLEARANCE_MULTI_PROBE': 2,
    'PROBING_HEATERS_OFF': "",  # Off prevents interference (induction).
    'PROBING_FANS_OFF': "",
    'PREHEAT_BEFORE_PROBING': None,
    # 'PROBING_NOZZLE_TEMP': 150,
    'PREHEAT_BEFORE_LEVELING': "",
    'LEVELING_NOZZLE_TEMP': 35,  # if PREHEAT_BEFORE_LEVELING
    'LEVELING_BED_TEMP': 63,  # if PREHEAT_BEFORE_LEVELING
    'GRID_MAX_POINTS_X': 5,
    # ^ GRID_MAX_POINTS_Y is set to GRID_MAX_POINTS_X by default.
    'EXTRAPOLATE_BEYOND_GRID': "",
    # 'LCD_BED_LEVELING': "",
    'LCD_BED_TRAMMING': None,
    # 'LEVEL_BED_CORNERS': None,  # renamed to LCD_BED_TRAMMING
    'Z_SAFE_HOMING': "",
    # endregion moved from R2X_14T and deleted redundant

    'Z_MIN_PROBE_REPEATABILITY_TEST': "",
    # 'AUTO_BED_LEVELING_BILINEAR': "",
    'G26_MESH_VALIDATION': "",
    'MESH_TEST_HOTEND_TEMP': 220,
    'MESH_TEST_BED_TEMP': 63,
    'MIN_SOFTWARE_ENDSTOP_Z': None,  # (formerly 'USE_ZMIN_PLUG': None)
    # ^ commented out for BLTouch as per
    #   <https://gist.github.com/wess/d48057846ab8272075521549562aac9e>
    'Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN': None,
    'MAX_SOFTWARE_ENDSTOPS': None,  # OFF since other 2 are hardware & this is 3
    # MAX_SOFTWARE_ENDSTOP_Z is already on by default, but off if hardware zmax
    'AUTO_BED_LEVELING_UBL': "",
    'UBL_MESH_WIZARD': "",
    # 'Z_MIN_ENDSTOP_INVERTING': False,  # moving-pin probe
    # 'Z_MIN_PROBE_ENDSTOP_INVERTING': False,  # moving-pin probe
    # ^ Changed to:
    'Z_MIN_ENDSTOP_HIT_STATE': "HIGH",
    'Z_MIN_PROBE_ENDSTOP_HIT_STATE': "HIGH",
    # ^ *Both* HIGH for BLTouch according to
    #   <https://all3dp.com/2/how-to-set-up-marlin-for-auto-bed-leveling/>
    # ^ "superset" of the previous bed leveling methods, with an
    #   "optimized line-splitting algorithm"
    #   -<https://marlinfw.org/docs/features/unified_bed_leveling.html>
    # 'MESH_BED_LEVELING': "",
    # ^ conflict: "Select only one of: MESH_BED_LEVELING,
    #   AUTO_BED_LEVELING_LINEAR, AUTO_BED_LEVELING_3POINT,
    #   AUTO_BED_LEVELING_BILINEAR or AUTO_BED_LEVELING_UBL."
    # TODO: (?) LCD_BED_LEVELING: "",
    # ^ "for ABL or MBL"
    #   "Include a guided procedure if manual probing is enabled"
}
# TODO: Add a neopixel option (NEOPIXEL_PIN)
BLTOUCH_C_COMMENTS = {
    'AUTO_BED_LEVELING_BILINEAR': (
        " // specified in the BLTouch Smart V3.1 manual"
        " but UBL supercedes it and MESH_BED_LEVELING"
    ),
    # 'USE_ZMIN_PLUG': '// commented out as per BLTouch Smart V3.1 manual',
    'Z_MIN_PROBE_USES_Z_MIN_ENDSTOP_PIN': (
        "  // commented as per the BLTouch Smart V3.1 manual",
    ),
    'Z_MIN_PROBE_PIN': [
        ("// ^ already defined as P0_10 in"
         " Marlin\\src\\pins\\lpc1768\\pins_BTT_SKR_V1_4.h"),
        ("//   (and Marlin\\src\\pins\\lpc1769\\pins\\BTT_SKR_V1_4_TURBO.h"
         " includes it)."),
    ],
    'NOZZLE_TO_PROBE_OFFSET': (
        "// -35,0,-2.56 works on FlexionHT (may drift to -2.7737),"
        " otherwise x is -36 such as for a hand-machined cooling block"
        " (z=+3.65 when not deployed; 6.07 using dial and 0.1mm feeler gauge),"
    ),
    'USE_PROBE_FOR_Z_HOMING': (
        '// Commented when using max endstop with probe?? (See <https://www.instructables.com/Dual-Z-Max-and-Probe-for-Z-Min/>)'
    ),
    # 'UBL_MESH_WIZARD': '         // Run several commands in a row to get a complete mesh',
}

BLTOUCH_C_A_VALUES = {
    # 'Z_STEPPER_AUTO_ALIGN': "",  # rec by BTT TFT if probe; for 2 Z *drivers*
    # ^ See printer-specific overrides that are set BEFORE BLTOUCH values
    'MESH_BED_LEVELING': "",
    'BLTOUCH_DELAY': 500,
    'BLTOUCH_FORCE_SW_MODE': "",
    'PROBE_OFFSET_WIZARD': "",
    'PROBE_OFFSET_WIZARD_START_Z': -4.0,
    'PROBE_OFFSET_WIZARD_XY_POS': "{ X_CENTER, Y_CENTER }",  # uncomment it only
    'ENDSTOPS_ALWAYS_ON_DEFAULT': None,  # MUST BE OFF!!! (See comments)
}


BLTOUCH_C_A_COMMENTS = {
    'PROBE_OFFSET_WIZARD_XY_POS': [
        ("      // ^ Set x to halfway (-35) between E0 and probe (-70)"
         " so they straddle the center"),
    ],
    'ENDSTOPS_ALWAYS_ON_DEFAULT': [
        '^ "stay on (by default) even when not homing"',
        ('  I tried this to avoid'
         ' <https://github.com/MarlinFirmware/Marlin/issues/25401>)'),
        '  but it *prevents homing from ever working* with BLTOUCH',
        ('  - The software endstop is apparently hit'
         ' (according to marlin error) around 17mm'
        '  before it can home!'),
    ]
}

R2X_14T_C_VALUES = {
    'STRING_CONFIG_H_AUTHOR': (
        '"(marlininfo by Jake Gustafson, BTT SKR V1.4 Turbo + TFT35'
        ' for Replicator 2X but with thermistors)"'
    ),  # + " // Who made the changes." comment is preserved by marlininfo
    'Z_PROBE_FEEDRATE_FAST': "(4*60)",
    'Z_PROBE_FEEDRATE_SLOW': "(Z_PROBE_FEEDRATE_FAST / 5)",  # default= ... / 2
    'CUSTOM_MACHINE_NAME': '"R2X 14T"',
    'SERIAL_PORT_2': -1,
    'MOTHERBOARD': "BOARD_BTT_SKR_V1_4_TURBO",
    'EXTRUDERS': 2,  # TODO: allow disabling the second extruder
    'HOTEND_OFFSET_X': "{ 0.0, 34.00 }",  # assumes EXTRUDERS is 2
    'HOTEND_OFFSET_Y': "{ 0.0, 0.00 }",  # assumes EXTRUDERS is 2
    'HOTEND_OFFSET_Z': "{ 0.0, -0.00 }",  # assumes EXTRUDERS is 2
    'TEMP_SENSOR_0': 11,  # 11 works for 100K Ohm thermistor such as
    # [HiLetgo NTC 3950](https://www.amazon.com/gp/product/B07V6YBFSY/
    # ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1)
    'TEMP_SENSOR_1': 11,  # removed later if nozzles == 1
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
    # 'USE_XMIN_PLUG': None,
    # 'USE_YMIN_PLUG': None,
    # 'USE_XMAX_PLUG': "",
    # 'USE_YMAX_PLUG': "",
    # ^ deprecated in bugfix-2.1.x <= 4c033c3e for MIN_SOFTWARE_ENDSTOPS:
    'MIN_SOFTWARE_ENDSTOPS': "",  # since always at least x & y are hardware
    'MIN_SOFTWARE_ENDSTOP_X': "",  # since max is hardware
    'MIN_SOFTWARE_ENDSTOP_Y': "",  # since max is hardware
    'MIN_SOFTWARE_ENDSTOP_Z': None,  # turned on later if bltouch_enabled
    'MAX_SOFTWARE_ENDSTOPS': "",  # Turned off if BLTouch (other 2 are hardware)
    'MAX_SOFTWARE_ENDSTOP_Z': "",  # commented (set to None) later if zmax
    'ENDSTOPPULLUP_ZMIN_PROBE': "",
    # 'X_MIN_ENDSTOP_INVERTING': True,
    # 'Y_MIN_ENDSTOP_INVERTING': True,
    # 'Z_MIN_ENDSTOP_INVERTING': True,
    # 'X_MAX_ENDSTOP_INVERTING': True,
    # 'Y_MAX_ENDSTOP_INVERTING': True,
    # 'Z_MAX_ENDSTOP_INVERTING': True,
    # 'Z_MIN_PROBE_ENDSTOP_INVERTING': False,
    # ^ True is replaced by LOW (default is HIGH):
    # 'X_MIN_ENDSTOP_HIT_STATE': "LOW",  # There is no hardware min
    'X_MAX_ENDSTOP_HIT_STATE': "LOW",
    # 'Y_MIN_ENDSTOP_HIT_STATE': "LOW",  # There is no hardware min
    'Y_MAX_ENDSTOP_HIT_STATE': "LOW",
    'Z_MIN_ENDSTOP_HIT_STATE': "LOW",  # BLTouch: HIGH
    # ^ HIGH for BLTouch according to
    #   <https://all3dp.com/2/how-to-set-up-marlin-for-auto-bed-leveling/>
    # ^ BLTouch is also LOW (formerly 'Z_MIN_PROBE_ENDSTOP_INVERTING': True)
    'Z_MAX_ENDSTOP_HIT_STATE': "HIGH",  # It only exists if zmax is custom
    # ^ High for some reason, even though factory one was inverted
    'Z_MIN_PROBE_ENDSTOP_HIT_STATE': "HIGH",
    # ^ These settings are necessary for the stock endstops that have circuits.
    #   For these, PULLUP defines (that raise a partial state to a binary
    #   state) shouldn't be necessary due to the circuits
    #   according to Ed's 3d Tech on [BTT SKR2 - Switch Endstop on SKR 2
    #   (Rev B)](https://www.youtube.com/watch?v=wwekaHOCHuk)
    #   Ed also mentions that you can check the current state of any
    #   endstop and they shouldn't be "TRIGGERED" unless pressed (They
    #   should be inverted if triggered when not pressed):
    #   M119
    'DISTINCT_E_FACTORS': "",
    'DEFAULT_AXIS_STEPS_PER_UNIT': (
        "{ 88.888889, 88.888889, 400, 92.61898734177215189873, 92.61898734177215189873 }"  # noqa: E501
    ), # 5 entries assumes EXTRUDERS is 2; See also comment
    'DEFAULT_MAX_FEEDRATE': "{ 200, 200, 5, 25, 25 }",  # assumes EXTRUDERS is 2
    'DEFAULT_MAX_ACCELERATION': "{ 2000, 2000, 200, 10000, 10000 }",
    # ^ 5 entries assumes EXTRUDERS is 2
    'DEFAULT_ACCELERATION': 850, # formerly 2000...but that's more jerky
    'DEFAULT_RETRACT_ACCELERATION': 2000,
    'DEFAULT_TRAVEL_ACCELERATION': 850,
    'ADVANCE_K': .44,  # Default .22 is right for most rigid materials
    # ^ 0 or S_CURVE_ACCELERATION is recommended by a Marlin comment for ABS!
    'DEFAULT_EJERK': 3.5,  # Higher is more jerky. May be used by linear advance
    'ALLOW_LOW_EJERK': "",
    # ^ "DEFAULT_EJERK value of <10. Recommended for direct drive"
    # 'S_CURVE_ACCELERATION': "",  # See comment
    'LIN_ADVANCE': "",  # Works OK on direct drive except for ABS
    # ^ See Marlin's own comments in unmodified Configuration.h itself
    'INVERT_X_DIR': True,
    'INVERT_Z_DIR': True,
    'INVERT_E1_DIR': True,
    'X_HOME_DIR': 1,
    'Y_HOME_DIR': 1,
    'X_BED_SIZE': 242,  # See comment
    'X_MIN_POS': -5,
    'Y_BED_SIZE': 153,  # See comment
    'Z_MAX_POS': 150,
    # ^ TODO: Z_MAX_POS may be as small as 123 with aluminum z axis assembly
    #   depending on screw tightness)
    'NOZZLE_PARK_POINT': "{ (X_MIN_POS + 10), (Y_MAX_POS - 10), 115 }",
    # ^ TODO: increase Z to 123 (as measured on screen by moving
    #   manually after homing; tried 115 before that) and see if is still ok.
    #   - Set to 0 until Marlin bug is fixed! See marlininfo issue
    #     [#22](https://github.com/poikilos/marlininfo/issues/22)
    'EEPROM_SETTINGS': "",
    'SDSUPPORT': "", # deprecated, handled by HASMEDIA macro now? Back in e41dc27
    # 'NEOPIXEL_PIN': "",  # Not tried, but may be a way to rig builtin ones
    'SPEAKER': "",  # *incompatible* with mega2560 (so only enabled here)
}


# TODO: add the comments from ZMAX_COMMENTS?
# Define min and max to prevent grinding the z axis follower
#   at the top of the range. All of these settings are
#   necessary to get Marlin to do it. See also:
# "z home dir must be 1 for z max homing."
# - Repetier
#   <forum.repetier.com/discussion/comment/30062/#Comment_30062>
# It is ok to home with the ZMAX endstop instead of the
#   probe (and necessary to use it with the probe as min):


R2X_14T_C_A_VALUES = {
    'EXPERIMENTAL_SCURVE': None,  # See Configuration.h comment for S_CURVE_ACCELERATION
    'Z_STEPPER_AUTO_ALIGN': None,  # rec by BTT TFT if probe; for 2 Z *drivers*
    'THERMAL_PROTECTION_HYSTERESIS': 8,
    'WATCH_TEMP_PERIOD': 25,
    'WATCH_TEMP_INCREASE': 7,
    # 'THERMAL_PROTECTION_BED_PERIOD': 20,  # default is 20
    'THERMAL_PROTECTION_BED_HYSTERESIS': 8,
    'WATCH_BED_TEMP_PERIOD': 70, # See WATCH_BED_TEMP_INCREASE comment.
    'WATCH_BED_TEMP_INCREASE': 3, # See comment.
    'HOTEND_IDLE_TIMEOUT': "",
    'HOTEND_IDLE_TIMEOUT_SEC': "(30*60)",  # long: don't interrupt UBL
    'HOTEND_IDLE_MIN_TRIGGER': 140,
    'HOTEND_IDLE_NOZZLE_TARGET': 100,
    'HOTEND_IDLE_BED_TARGET': 43,
    'MULTI_NOZZLE_DUPLICATION': "",
    'ADAPTIVE_STEP_SMOOTHING': "",
    'BABYSTEPPING': "",
    'DOUBLECLICK_FOR_Z_BABYSTEPPING': "",
    # 'BABYSTEP_ZPROBE_OFFSET': "",  # conflicts with MESH_BED_LEVELING
    'LIN_ADVANCE': "",  # 0 for ABS (only Klipper pressure advance works for ABS, not Marlin linear advance)!
    'ALLOW_LOW_EJERK': "",  # allow <10 (recommended for direct drive in Marlin's own comments)
    'INPUT_SHAPING_X': "",
    'INPUT_SHAPING_Y': "",
    'SHAPING_MENU': "",
}

# TODO: implement per-machine comments.
R2X_14T_C_COMMENTS = {
    'CUSTOM_MACHINE_NAME': [
        '// max length BTT TFT24:        "                     "'
    ],
    'TEMP_SENSOR_1': ' // 2ND NOZZLE',
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
    'X_BED_SIZE': [
        ' // ^ formerly 236; 242 would center the nozzle on the edge with FlexionHT,',
        ' //   or still be on with that plus FilaPrint. 243 allows purging and wiping',
        ' //   to occur *off the edge to keep entire build width clean*',
        ' //   but using a negative number for X_MIN_POS prevents slicing problems',
        ' //   Actual surface X: 248.5',
    ],
    'X_MIN_POS': "Allow left nozzle to go off bed for purge & wipe.",
    'Y_BED_SIZE': ' // 133-134 with custom front duct; 152 factory spec; 153 measured but may touch x rail & push motor back 1 step! (actual surface Y: 165)',
    'DEFAULT_AXIS_STEPS_PER_UNIT': [
        '/*',
        'Extrusion:',
        '- Used factory setting 96.275 then calibrated it',
        ' (it extruded 95/100 mm, so result is 91.46125)',
        '- Using that value with the FlexionHT though,',
        '  (hot, using a 300mm mark I made above the extruder inlet)',
        '  I extruded 200mm and got 197.5, so the result is',
        '  92.61898734177215189873.',
        'Movement:',
        ('> The Replicator 2 and 2x use 18 tooth GT2 pulleys,'
         ' 1/16 microstepping, and 200 steps/rev steppers.'
         ' That makes the proper steps/mm value 88.888889.'),
        ('> Note that Makerbot used ~88.56 steps/mm in their defaults,'
         ' which is the value you get if you calculate from the belt+pulley'
         ' pitch diameter from the Gates GT2 specs. But this is the value'
         ' you use for calculating belt length required in a closed loop,'
         ' not for steps/mm. The 88.88... number is more accurate.'),
        "> by Ryan Carlyle Mar 2 '16 at 20:15",
        ("> - Hey once again, what about z axis then?"
         " – Anton Osadchy Mar 7 '16 at 17:47"),
        ("> - Z is 400 steps/mm. (8mm lead, 1/16 microstepping,"
         " 200 steps/mm motor.) Sidenote, make sure you don't over-drive"
         " the Z stepper with plug-in drivers, it's only rated to about 0.4A."
         " – Ryan Carlyle Mar 7 '16 at 19:15"),
        ("> - @RyanCarlyle FYI minor typo above, you say 200 steps/mm"
         " for Z but I think you mean steps/rev since you already state"
         " Z is 400 steps/mm. Thank you for accurate numbers though!"
         " – guru_florida Aug 22 '20 at 15:12"),
        '',
        '-<https://3dprinting.stackexchange.com/a/678>',
        '*/',
    ],
    'S_CURVE_ACCELERATION': [
        "// ^ S_CURVE_ACCELERATION conflicts with LIN_ADVANCE unless",
        "//   EXPERIMENTAL_SCURVE; LINEAR acceleration is",
        "//   counterproductive at least for ABS on direct drive",
        "//   (Marlin's calibration test only looks correct on K=0 line).",
    ],
    'ADVANCE_K': "The default .22 is ok for most materials, but use .44 for ATARAXIA ART Flexible PLA+, bed=30C, nozzle=170C. '(mm) Compression length applying to all extruders'",  # noqa: E501
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
    # 'WATCH_BED_TEMP_INCREASE': "See WATCH_BED_TEMP_INCREASE comment.",
    'WATCH_BED_TEMP_INCREASE': [
        ("  // ^ Based on approximate stopwatch readings,"
         " the Replicator 2X bed heats"),
        "  //   at 1C per 8s to up to about 27s at first!",
        "  //   When the bed first starts heating, it is very slow,",
        "  //   even if you reset it and start around 35C.",
        "  //   Between 80 and 110, it can still do thermal shutdown",
        "  //   at WATCH_BED_TEMP_PERIOD 60 WATCH_BED_TEMP_INCREASE 4.",
    ],
}


LOW_CUSTOM_ZMAX_VALUES = {
    'Z_MAX_ENDSTOP_HIT_STATE': "LOW",
    'MAX_SOFTWARE_ENDSTOP_Z': None,
    'MAX_SOFTWARE_ENDSTOPS': None,
    # ^ Moved to BLTOUCH config.
    'Z_MAX_POS': 150,  # actual: 150 (factory spec = custom zmax (after worn??))
    # Set bigger than actual to test custom zmax
    # No comments below seem to matter actually.
    # ^ Don't set Z_MAX_POS too high or Marlin might give up (It
    #   may determine the bed is floating more than 25 mm above
    #   the endstop if set to the factory build volume's 155
    #   height).
    #   Z_MAX_POS is actually about 148.7 (to 150.7...worn in??) with Poikilos'
    #   printable ZMAX endstop holder (and the FilaPrint bed
    #   treatment), but setting it to that
    #   may cause Marlin to give up if you get to 0 before the
    #   probe triggers (such as if your springs aren't tightened
    #   as much as mine)--remember, homing is done at max then
    #   probing happens by approaching 0 from there.
}


'''

# This is wrong, apparently. See BLTouch config instead.
use_z_probe_for_homing = False
if use_z_probe_for_homing:
    thisMarlin.set_c("USE_PROBE_FOR_Z_HOMING", None)
    thisMarlin.set_c("Z_HOME_DIR", 1)
else:
    thisMarlin.set_c("USE_PROBE_FOR_Z_HOMING", "")
    thisMarlin.set_c("Z_HOME_DIR", -1)
'''


LOW_CUSTOM_ZMAX_COMMENTS = {
    'Z_MAX_ENDSTOP_HIT_STATE':
        "LOW (formerly Z_MAX_ENDSTOP_INVERTING true + USE_ZMAX_PLUG)",
    'MAX_SOFTWARE_ENDSTOPS': [
        "  // ^ X&Y are hardware, so *all* are if zmax_answer",
        "  // Note that ZMAX_PLUG is POWERDET according to",
        "  // Marlin\Marlin\src\pins\lpc1768\pins_BTT_SKR_V1_4.h",
        "  // *not* on the same row as the ZMIN plugs according to the",
        "  // board diagram, but is the one next to EXP1.",
        "  // *The pin must be enabled* (See Configuration_adv.h)!",
    ]
}


MACHINES_C_COMMENTS = {
    'A3S': A3S_C_COMMENTS,
    'R2X_14T': R2X_14T_C_COMMENTS,
}

MACHINES_C_A_COMMENTS = {
    'A3S': A3S_C_A_COMMENTS,
    'R2X_14T': R2X_14T_C_A_COMMENTS,
}

MACHINES_C_VALUES = {
    'A3S': A3S_C_VALUES,
    'R2X_14T': R2X_14T_C_VALUES,
}

MACHINES_C_A_VALUES = {
    'A3S': A3S_C_A_VALUES,
    'R2X_14T': R2X_14T_C_A_VALUES,
}

verbosity = 0
verbosities = [True, False, 0, 1, 2]


def set_verbosity(level):
    global verbosity
    if level not in verbosities:
        raise ValueError("level must be one of {}".format(verbosities))
    verbosity = level
    echo0("verbosity={}".format(verbosity))


def get_verbosity():
    return verbosity


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

    C_REL = os.path.join("Marlin", "Configuration.h")
    C_A_REL = os.path.join("Marlin", "Configuration_adv.h")
    PINS_BTT_SKR_V1_4_REL = os.path.join("Marlin", "src", "pins",
                                         "lpc1768", "pins_BTT_SKR_V1_4.h")
    TRANSFER_RELPATHS = [
        "platformio.ini",
        C_REL,
        C_A_REL,
        PINS_BTT_SKR_V1_4_REL,
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

    def __init__(self, path, repo=None):
        '''
        Keyword arguments:
        repo -- an existing git.Repo instance that is equivalent to path
            (will be generated automatically from path, or from parent
            of path if path is a Marlin/Marlin directory).
        '''
        self._loaded_repo_path = None
        # sub = os.path.split(path)[1]
        MarlinMarlin = os.path.join(path, "Marlin")
        self.c_path = os.path.join(path, MarlinInfo.C_REL)
        self.c_a_path = os.path.join(path, MarlinInfo.C_A_REL)
        self.driver_names = None
        self.file_metas = {}
        self._changed = []
        self._not_changed = []  # ECLineInfo list

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
                ''.format(self.c_path, "in ..")
            )
            return 1
        if not os.path.isfile(self.c_path):
            raise FileNotFoundError(
                'Error: "{}" does not exist (also tried "{}")'
                ''.format(self.c_a_path, "in ..")
            )
            return 1
        self.mm_path = os.path.dirname(self.c_path)
        self.m_path = os.path.dirname(self.mm_path)

        self.repo = None
        if repo is None:
            self.load_repo()
        else:
            self.repo = repo

        for relpath in MarlinInfo.TRANSFER_RELPATHS:
            file_path = os.path.join(self.m_path, relpath)
            if os.path.isfile(file_path):
                self.file_metas[relpath] = SourceFileInfo(self.m_path, relpath)
            else:
                # The file is optional (such as "platformio.ini"
                #   or files in "/pins") if there wasn't an error yet.
                echo1('* there is no "{}"'.format(file_path))

    def load_repo(self):
        '''
        Load the repo at self.m_path (only if that is not already loaded
        as self.repo).
        '''
        if self.m_path is None:
            raise ValueError("self.m_path must be set before load_repo.")
        if self._loaded_repo_path == self.m_path:
            return True
        try:
            self._loaded_repo_path = None
            if self.repo is not None:
                del self.repo
                self.repo = None
            repo = Repo(self.m_path)
            if not repo.bare:
                self.repo = repo
                self._loaded_repo_path = self.m_path
                return True
            else:
                echo0('Warning: diff features will not be available '
                      ' since "{}" is a bare repo.'.format(self.m_path))
        except git.exc.InvalidGitRepositoryError:
            echo0('Warning: diff features will not be available '
                  ' since "{}" is not a repo.'.format(self.m_path))
        return False

    def backup_dir(self):
        '''
        Get the path (string) of the directory where a backup of the
        current commit resides.
        '''
        backups_dir = os.path.join(MY_CONFIG_DIR, "backup")
        repo_user_path, repo_name = os.path.split(self.m_path)
        repo_user = os.path.split(repo_user_path)[1]
        # ^ such as MarlinFirmware or someone who forked Marlin
        return os.path.join(backups_dir, repo_user, repo_name,
                            str(self.repo.active_branch),
                            self.short_commit())

    def backup_config(self):
        '''
        Backup all of the Marlin configuration files, but only if they
        are unchanged.

        Raises:
        RuntimeError if the file is changed (doesn't match git index)
        but there is not already a backup of it in self.backup_dir().
        '''
        if not self.load_repo():
            return False

        backup_dir = self.backup_dir()
        changed_relpaths = [c.a_path for c in self.repo.index.diff(None)]
        # a and b are the left and right side of the diff.
        for relpath in MarlinInfo.TRANSFER_RELPATHS:
            old = os.path.join(self.m_path, relpath)
            bak = os.path.join(backup_dir, relpath)
            bak_dir = os.path.dirname(bak)
            if not os.path.isdir(bak_dir):
                os.makedirs(bak_dir)

            if not os.path.isfile(bak):
                if relpath in changed_relpaths:
                    raise RuntimeError(
                        '"{}" could not be backed up because it was already'
                        ' changed. Revert it before running this file, so'
                        ' that a clean copy can be created at "{}".'
                        ''.format(old, bak)
                    )
                '''
                else:
                    raise NotImplementedError(
                        '"{}" is not in {}'
                        ' (should be no problem if pathing is correct)'
                        ''.format(relpath, changed_relpaths))
                '''
                shutil.copy(old, bak)
                echo0('- backed up "{}"'.format(bak))
            else:
                echo0('- kept existing "{}"'.format(bak))
        return True

    def short_commit(self):
        if not self.load_repo():
            return None
        return str(self.repo.commit())[:7]


    @classmethod
    def transfer_paths_in(cls, roots):
        '''
        Get the configuration file paths for the given roots. If any
        item of roots is not a directory it will not be modified. If
        you are trying to modify a single directory, still put it in
        a list such as `subs = transfer_paths_in([path])`.
        '''

        results = []
        for relpath in cls.TRANSFER_RELPATHS:
            parts = roots.copy()
            for i in range(len(parts)):
                if os.path.isdir(parts[i]):
                    parts[i] = os.path.join(parts[i], relpath)
            results.append(parts)
        return results

    def get_c(self, name):
        '''
        Get a a 3-long tuple with the value of the named #define from
        Marlin/Configuration.h along with the line number and error
        if any.
        '''
        # relpath = MarlinInfo.C_REL
        # fi = self.file_metas[relpath]
        return get_cdef(self.c_path, name)

    def get_c_a(self, name):
        '''
        Get a a 3-long tuple with the value of the named #define from
        Marlin/Configuration_adv.h along with the line number and error
        if any.
        '''
        # relpath = MarlinInfo.C_A_REL
        # fi = self.file_metas[relpath]
        return get_cdef(self.c_a_path, name)

    def get_relative(self, path):
        bad_start = self.m_path + os.path.sep
        relpath = path
        if relpath.startswith(bad_start):
            relpath = relpath[len(bad_start):]
        return relpath

    def get_cached_rel(self, name, relpath):
        '''
        Get a cached value.

        Sequential arguments:
        name -- The name of the #define.
        relpath -- The relative path within Marlin such as
            "Marlin/Configuration.h". If the path starts with
            self.m_path+"/", that portion will be removed to allow the
            file_metas lookup to still work.
        '''
        if name is None:
            raise ValueError("You must provide the name to get_cached_rel.")
        relpath = self.get_relative(relpath)
        fi = self.file_metas[relpath]
        return fi.get_cached(name)

    def get_line(self, line_index, relpath):
        relpath = self.get_relative(relpath)
        fi = self.file_metas[relpath]
        # v, line_n, got_key, err = fi.get_cached(None, line_index=line_index)
        return fi._lines[line_index]

    def get_cached_c(self, name):
        return self.get_cached_rel(name, MarlinInfo.C_REL)

    def get_cached_c_a(self, name):
        return self.get_cached_rel(name, MarlinInfo.C_A_REL)

    def get_confs_versions(self):
        '''
        Get a tuple of the values CONFIGURATION_H_VERSION and
        CONFIGURATION_ADV_H_VERSION as strings.
        '''
        return (
            self.get_c("CONFIGURATION_H_VERSION")[0],
            self.get_c_a("CONFIGURATION_ADV_H_VERSION")[0],
        )

    def copy_to(self, repo_path):
        '''
        Copy configs from mm_path to os.path.join(repo_path, "Marlin")
        --the Marlin/Marlin subdirectory will be created if it doesn't
        exist, where Marlin/ is repo_path.
        '''
        results = []
        if not os.path.isdir(repo_path):
            raise FileNotFoundError('"{}" does not exist.'.format(repo_path))
        dest_mm_path = os.path.join(repo_path, "Marlin")
        if not os.path.isdir(dest_mm_path):
            os.mkdir(dest_mm_path)
        for src in MarlinInfo.TRANSFER_RELPATHS:
            srcPath = os.path.join(self.m_path, src)
            dstPath = os.path.join(repo_path, src)
            if os.path.isfile(srcPath):
                dstParent = os.path.dirname(dstPath)
                if not os.path.isdir(dstParent):
                    os.makedirs(dstParent)
                shutil.copy(srcPath, dstPath)
                results.append(dstPath)
        return results

    def drivers_dict(self):
        results = {}
        for name in MarlinInfo.DRIVER_NAMES:
            v, line_n, got_name, err = self.get_cached_c(name)
            if err == COMMENTED_DEF_WARNING:
                continue
            elif v is not None:
                results[name] = v
        return results

    def save_changes(self):
        '''
        Only save if there are unsaved changes made using the
        set_ and insert_ methods or methods that use them. There will be
        no changes if the calls used values that were the same as the
        previous values.
        '''
        count = 0
        for relpath, fi in self.file_metas.items():
            echo1('saving "{}"'.format(fi.full_path()))
            this_count = fi.save_changes()
            echo0('* saved {} change(s) to "{}"'
                  ''.format(this_count, fi.full_path()))
            count += this_count
        return count

    def set_c(self, name, value, comments=None):
        '''
        This operates on MarlinInfo.C_REL.
        For documentation see SourceFileInfo's set_cached method.
        '''
        relpath = MarlinInfo.C_REL
        fi = self.file_metas[relpath]
        lines, unaffected_items = fi.set_cached(name, value, comments=comments)
        self._changed += lines
        self._not_changed += unaffected_items
        if len(lines) > 0:
            # echo2("{}: #define {} {}".format(fi.full_path(), name, value))
            for line in lines:
                echo2("{}: `{}`".format(fi.full_path(), line))
        else:
            echo2("(skipped) {}: {} to {}".format(fi.full_path(), name, value))

    def add_not_changed_lines(self, lines, relpath):
        d = cdefs_to_d(None, lines=lines)
        for key, value in d.items():
            self._not_changed.append(ECLineInfo(
                key,
                None,
                v=value,
                # t="string",
                # i=None,  # Line number or other index
                commented=value is None,
                cm="//",
                path=relpath,
                orphan=True,
            ))


    def set_c_a(self, name, value, comments=None):
        '''
        This operates on MarlinInfo.C_A_REL.
        For documentation see SourceFileInfo's set_cached method.
        '''
        relpath = MarlinInfo.C_A_REL
        fi = self.file_metas[relpath]
        lines, unaffected_items = fi.set_cached(name, value, comments=comments)
        for line in lines:
            echo2("{}: `{}`".format(fi.full_path(), line))
        self._changed += lines
        self._not_changed += unaffected_items


    def set_multiple_c(self, d, comment_d=None):
        '''
        Sequential arguments:
        d -- a dict with several keys and values to change in the Marlin
            Configuration.h.
        comment_d -- a dict where each key corresponds to a key in d and
            the value is a string or string list (For details on the
            individual value itself, see the MarlinInfo set_c
            documentation for the "comments" argument).
        '''
        for key, value in d.items():
            comments = None
            if comment_d is not None:
                comments = comment_d.get(key)
            self.set_c(key, value, comments=comments)
            # ^ set_c handles self._changed and self._not_changed

    def set_multiple_c_a(self, d, comment_d=None):
        '''
        Sequential arguments:
        d -- a dict with several keys and values to change in the Marlin
            Configuration.h.
        '''
        for key, value in d.items():
            # Overwrite tpu items that are in the third entry temporarily.
            comments = None
            if comment_d is not None:
                comments = comment_d.get(key)
            self.set_c_a(key, value, comments=comments)
            # ^ set_c handles self._changed and self._not_changed

    def set_pin(self, name, value, comments=None):
        '''
        This operates on MarlinInfo.PINS_BTT_SKR_V1_4_REL.
        For documentation see SourceFileInfo's set_cached method.
        '''
        relpath = MarlinInfo.PINS_BTT_SKR_V1_4_REL
        if relpath not in self.file_metas:
            raise FileNotFoundError(
                '"{}" is missing but is required for this configuration.'
                ''.format(os.path.join(self.mm_path, relpath))
            )
        fi = self.file_metas[relpath]
        # new_line = None
        lines, unaffected_items = fi.set_cached(name, value, comments=comments)
        self._changed += lines
        self._not_changed += unaffected_items
        if len(lines) > 0:
            return True
        return False

    def insert_c(self, lines, after=None, before=None):
        '''
        Insert into self.c_path (or lines if present).
        For documentation see SourceFileInfo's insert_cached method.

        Returns:
        True if success, False if failed.
        '''
        relpath = MarlinInfo.C_REL
        fi = self.file_metas[relpath]
        if fi.insert_cached(lines, after=after, before=before):
            self._changed += lines
            return True
        else:
            self.add_not_changed_lines(lines, relpath)
        return False

    def insert_c_a(self, lines, after=None, before=None):
        '''
        Insert into self.c_a_path (or lines if present).
        For documentation see SourceFileInfo's insert_cached method.

        Returns:
        True if success, False if failed.
        '''
        relpath = MarlinInfo.C_A_REL
        fi = self.file_metas[relpath]
        if fi.insert_cached(lines, after=after, before=before):
            self._changed += lines
            return True
        else:
            self.add_not_changed_lines(lines, relpath)
        return False


    def insert_multiple_c(self, lines_for_flags):
        '''
        Sequential arguments:
        lines_for_flags -- a dictionary where each key is a flag to
            find in the marlin Configuration.h after
            which to insert the value.
        '''
        for flag, lines in lines_for_flags.items():
            self.insert_c(lines, after=flag)
            # ^ handles self._changed and self._not_changed


    def insert_multiple_c_a(self, lines_for_flags):
        '''
        Sequential arguments:
        lines_for_flags -- a dictionary where each key is a flag to
            find in the marlin Configuration.h after
            which to insert the value.
        '''
        for flag, lines in lines_for_flags.items():
            self.insert_c_a(lines, after=flag)
            # ^ handles self._changed and self._not_changed

    def insert_pin_lines(self, lines, after=None, before=None):
        '''
        Insert into self.c_a_path (or lines if present).
        For documentation see SourceFileInfo's insert_cached method.

        Returns:
        True if success, False if failed.
        '''
        relpath = MarlinInfo.PINS_BTT_SKR_V1_4_REL
        fi = self.file_metas[relpath]
        if fi.insert_cached(lines, after=after, before=before):
            self._changed += lines
            return True
        else:
            self.add_not_changed_lines(lines, relpath)
        return False

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
        self.set_c(self.driver_names, driver_type)


# from https://github.com/poikilos/DigitalMusicMC
# and https://github.com/poikilos/blnk
# and https://github.com/poikilos/linux-preinstall
def which(cmd):
    paths_str = os.environ.get('PATH')
    if paths_str is None:
        echo1("Warning: There is no PATH variable, so returning {}"
              "".format(cmd))
        return cmd
    paths = paths_str.split(os.path.pathsep)
    for path in paths:
        echo1("looking in {}".format(path))
        tryPath = os.path.join(path, cmd)
        if os.path.isfile(tryPath):
            return tryPath
        else:
            echo1("There is no {}".format(tryPath))
    return None


POST_MERGE_DOC_FMT = '''
After merging:
- Close any slicers, Pronterface, or anything else that may use the USB
  port where the 3D Printer is connected.
- Connect the 3D printer via USB and open "{marlin_path}" in Arduino IDE.
- *Unplug the serial connector* from the screen if using an MKS Gen-L V1
  to avoid bricking the screen by passing the board firmware to it!
- Choose the correct hardware for "Board" "Processor" and "Port"
  (all 3 are in the "Tools" menu).
- Click "Upload" (right arrow) to compile & upload.
- After it says "Finished Upload", reconnect the LCD screen.
- Use the screen to reset the firmware settings
  (press "Reset" on the warning, or find the reset option), then save.
  Otherwise, open Pronterface, choose the port, connect, then run:
M502;
M500;
- In Pronterface or your start g-code in your slicer, you can
  set the linear advance to the correct value of your filament.
  See <https://marlinfw.org/tools/lin_advance/k-factor.html>
  or <https://github.com/poikilos/LinearAdvanceTowerGenerator>
  for calibration code and steps to obtain the correct K value such as:
; viewcurrent value:
M900;
; HDglass, with 1.9mm ID x 680mm bowden tube:
M900 K0.8;
M500;
Reboot (and install firmware from SDcard bin file if present):
M997;

Opening a slicer while printing from the SD card may freeze the print
on MKS screens (confirmed on TFT28 V4.0 with firmware 3.0.2).
Unplugging the USB cable while printing from the SD card is ideal.

'''


def in_any(haystacks, needle):
    for haystack in haystacks:
        if needle in haystack:
            return True
    return False


def c_val_hr(v):
    '''
    Get a human-readable representation of an encoded C value.
    '''
    vMsg = toPythonLiteral(v)
    if v == "":
        vMsg = "undefined"
    elif v is None:
        vMsg = "undefined"
    return vMsg

def get_repo(path):
    repo = None
    try:
        repo = Repo(path)
    except git.exc.InvalidGitRepositoryError:
        pass
    if (repo is not None) and repo.bare:
        echo0("The repo is bare.")
        repo = None
    if repo is None:
        # echo0('  branch: "{}"'.format())
        sys.stderr.write(
            "Error: You must run this from a destination Marlin repo"
            " or specify one (or Marlin/Marlin directory)."
        )
        try_dst = None
        HOME = pathlib.Path.home()
        try_dsts = [
            os.path.join(HOME, "Downloads", "git", "MarlinFirmware", "Marlin"),
            os.path.join(HOME, "git", "MarlinFirmware", "Marlin"),
        ]
        found_dst = None
        for try_dst in try_dsts:
            if os.path.isdir(try_dst):
                found_dst = try_dst
                break
        if found_dst is not None:
            sys.stderr.write(
                ' such as via:\n  {} "{}"\n'.format(sys.argv[0], found_dst)
            )
        else:
            sys.stderr.write(".\n")
        sys.stderr.flush()
    return repo

def main():
    try:
        srcMarlin = MarlinInfo(os.getcwd())
        # ^ If in_place, then above is changed to dstMarlin.backup_dir()
    except FileNotFoundError as ex:
        echo0(str(ex))
        echo0("You must run this from a Marlin repo"
              " (or Marlin/Marlin directory).")
        return 1
    dst_repo_path = None
    options = {}
    value_arg_keys = {}
    tmp_keys = [
        'machine',
        'driver-type',
        'T0',
        'nozzles',
    ]
    BOOLEAN_KEYS = [
        'zmax',
    ]
    echo1()
    echo1("CHECKING FOR OPTIONS...")
    echo1()
    for key in tmp_keys:
        value_arg_keys["--" + key] = key
    key = None
    in_place = True
    for argI in range(1, len(sys.argv)):
        arg = sys.argv[argI]
        if key is not None:
            options[key] = arg
            key = None
        elif arg.startswith("--"):
            next_key = value_arg_keys.get(arg)
            tmp_key = arg[2:]
            if arg == "--verbose":
                set_verbosity(1)
            elif arg == "--debug":
                set_verbosity(2)
            elif tmp_key in BOOLEAN_KEYS:
                options[tmp_key] = True
            elif next_key is not None:
                key = next_key
                echo1("using setting {} via {}"
                      "".format(next_key, arg))
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
                in_place = False
            else:
                usage()
                echo0('You specified an extra argument: "{}"'
                      ''.format(arg))
                return 1
    echo1("options={}".format(options))

    repo = None
    if dst_repo_path is not None:
        repo = get_repo(dst_repo_path)
    else:
        try_current_path = os.path.realpath(".")
        repo = get_repo(try_current_path)
        if repo is not None:
            dst_repo_path = try_current_path

    if repo is None:
        # An error should have already been shown in this case.
        return 1

    echo0("Stats:")
    # echo0(dir(repo))
    echo0('  active_branch="{}"'.format(repo.active_branch))
    # echo0('  tag="{}"'.format(repo.tag("refs/tags/"+versionTagStr)))
    # echo0('  tree="{}"'.format(repo.tree()))  # hash
    # echo0('  head="{}"'.format(repo.head))  # usually "HEAD"
    # echo0('  remote="{}"'.format(repo.remote()))  # usually "origin"
    echo0('  commit="{}"'.format(repo.commit()))
    changed = list(repo.index.diff(None))
    if len(changed) > 0:
        echo0("  changed:")
        for item in changed:
            echo0('  - "{}"'.format(item.a_path))
    else:
        echo0("  changed: None")

    # If the code gets this far, dst_repo_path is guaranteed
    #   either by sequential arg
    #   *or* if "." is a repo (see case above).

    dstMarlin = MarlinInfo(dst_repo_path, repo=repo)
    if not dstMarlin.backup_config():
        raise RuntimeError(
            "backup_config() failed. See output above for more info."
        )
    if in_place:
        try:
            srcMarlin = MarlinInfo(dstMarlin.backup_dir())
        except FileNotFoundError as ex:
            echo0()
            echo0(
                'The backup did not produce a valid Marlin at "{}": {}'
                ''.format(dstMarlin.backup_dir(), ex)
            )
            raise
        echo0('Modifying in place (setting source to backup: "{}")'
              ''.format(srcMarlin.m_path))
    # else it was already set to os.getcwd()

    echo0('dst_repo_path="{}"'.format(dst_repo_path))
    echo0('source Configuration.h, _adv versions: {}'
          ''.format(srcMarlin.get_confs_versions()))
    echo0('destination Configuration.h, _adv versions: {}'
          ''.format(dstMarlin.get_confs_versions()))
    if dstMarlin.get_confs_versions() != srcMarlin.get_confs_versions():
        echo0("Error: The configuration versions are incompatible")
        echo0(" ({} != {}) First try:".format(
            dstMarlin.get_confs_versions(),
            srcMarlin.get_confs_versions(),
        ))
        echo0('  meld "{}" "{}"'.format(srcMarlin.mm_path, dstMarlin.mm_path))
        return 1
    this_marlin_name = os.path.split(srcMarlin.m_path)[1]
    this_data_path = os.path.join(MY_CACHE_DIR, "tmp", this_marlin_name)
    if os.path.isdir(this_data_path):
        shutil.rmtree(this_data_path)
    if not os.path.isdir(this_data_path):
        os.makedirs(this_data_path)
    results = srcMarlin.copy_to(this_data_path)
    if len(results) > 0:
        for result in results:
            echo0('* wrote "{}"'.format(result))
    else:
        raise FileNotFoundError(
            "There were no files to transfer (looked for: {})."
            "".format(MarlinInfo.TRANSFER_RELPATHS)
        )
    thisMarlin = MarlinInfo(this_data_path)

    driver_types = ["A4988", "TMC2209"]  # or "TMC2130" etc.
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

    # Add TPU & PETG to the preheat menu
    # (adding petg_lines won't work if tpu_lines_flag isn't found,
    # since the last line of tpu_lines_flag is the flag for petg_lines):
    thisMarlin.insert_c(tpu_lines, after=tpu_lines_flag)
    thisMarlin.insert_c(petg_lines, after=petg_lines_flag)
    thisMarlin.insert_c(AAFPP_LINES, after=AAFPP_lines_flag)

    thisMarlin.set_multiple_c(MOVED_ABS)
    thisMarlin.set_multiple_c(MOVED_TPU)
    thisMarlin.set_multiple_c(
        POIKILOS_C_VALUES,
        comment_d=POIKILOS_C_COMMENTS,
    )
    thisMarlin.set_multiple_c_a(
        POIKILOS_C_A_VALUES,
        comment_d=POIKILOS_C_A_COMMENTS,
    )
    # previous_verbosity = get_verbosity()
    # set_verbosity(2)
    echo2("* setting Configuration.h values for {}".format(machine))
    thisMarlin.set_multiple_c(
        MACHINES_C_VALUES[machine],
        comment_d=MACHINES_C_COMMENTS.get(machine),
    )
    # set_verbosity(previous_verbosity)
    echo2("* setting Configuration_adv.h values for {}".format(machine))
    thisMarlin.set_multiple_c_a(
        MACHINES_C_A_VALUES[machine],
        comment_d=MACHINES_C_A_COMMENTS.get(machine),
    )
    thisMarlin.insert_multiple_c(TOP_C_LINES.get(machine))
    thisMarlin.insert_multiple_c_a(TOP_C_A_LINES.get(machine))

    if machine == "R2X_14T":
        driver_types = ["TMC2209"]

        if driver_type is not None:
            if driver_type not in driver_types:
                raise ValueError(
                    "For {} the driver_type {}"
                    " should instead be one of: {}"
                    "".format(machine, driver_type, driver_types)
                )
            print("driver_type={}".format(driver_type))
        else:
            driver_type = driver_types[0]
            print("# automatically selected for {}:".format(machine))
            print("--driver-type {}".format(driver_type))

        thisMarlin.driver_names = [
            'X_DRIVER_TYPE',
            'Y_DRIVER_TYPE',
            'Z_DRIVER_TYPE',
            'E0_DRIVER_TYPE',
            'E1_DRIVER_TYPE',  # removed later if nozzles == 1
        ]

        # Always use BTT TFT values for R2X_14T (ok for TFT35 as well):
        thisMarlin.set_multiple_c(BTT_TFT_C_VALUES,
                                  comment_d=BTT_TFT_C_COMMENTS)
        thisMarlin.set_multiple_c_a(BTT_TFT_C_A_VALUES,
                                    comment_d=BTT_TFT_C_A_COMMENTS)
        bltouch_enabled = True
        if bltouch_enabled:
            thisMarlin.set_multiple_c(BLTOUCH_C_VALUES,
                                      comment_d=BLTOUCH_C_COMMENTS)
            thisMarlin.set_multiple_c_a(BLTOUCH_C_A_VALUES,
                                        comment_d=BLTOUCH_C_A_COMMENTS)

        th_answer = options.get("T0")
        if th_answer is None:
            while True:
                th_answer = input("Are you using 0 or 1 for T0"
                                  " (0:TH0 or 1:TH1)? ")
                known_th_pins = ["0", "1"]  # default for T0
                if th_answer not in known_th_pins:
                    print("Error: Only {} are recognized.".format(known_th_pins))
                    continue
                    # raise NotImplementedError(
                    #     "Only pins {} are implemented.".format(known_th_pins)
                    # )
                break
        if th_answer == "1":
            # -#define TEMP_1_PIN                      P0_23_A0  // A0 (T0) - (67) - TEMP_1_PIN
            # -#define TEMP_BED_PIN                    P0_25_A2  // A2 (T2) - (69) - TEMP_BED_PIN            #define TEMP_0_PIN P0_23_A0
            # +#define TEMP_0_PIN P0_23_A0
            # +#define TEMP_1_PIN P0_24_A1
            # +#define TEMP_BED_PIN P0_25_A2
            # ^ TEMP_0_PIN is defined in
            #   Marlin\src\pins\lpc1768\pins_BTT_SKR_common.h
            #   but its value will be switched with TEMP_1_PIN in this patch.
            thisMarlin.set_pin("TEMP_1_PIN", "P0_24_A1")
            new_lines = ["#define TEMP_0_PIN P0_23_A0"]
            thisMarlin.insert_pin_lines(new_lines, before="TEMP_1_PIN")

            print("* The TH0 port will be avoided due to --T0 1.")
            if options.get('nozzles') is not None:
                if options.get('nozzles') != 1:
                    raise ValueError(
                        "You can only use 1 nozzle because you said"
                        " to avoid a damaged TH0, but --nozzles is set to"
                        " {}.".format(options.get('nozzles'))
                    )
            options['nozzles'] = "1"
        elif th_answer == "0":
            print("* The default --T0 TH0 will be assumed (no code changes).")
        user_nozzles = options.get('nozzles')
        nozzles = None
        if user_nozzles is None:
            nozzles = 2
        else:
            nozzles = int(user_nozzles)
        if nozzles == 1:
            thisMarlin.set_c_a("MULTI_NOZZLE_DUPLICATION", None)
            thisMarlin.set_c("EXTRUDERS", 1)
            thisMarlin.set_c("DISTINCT_E_FACTORS", None)
            # All of the following should have only one extruder element
            #   instead of the last value being duplicated in the case
            #   of having two:
            thisMarlin.set_c("DEFAULT_AXIS_STEPS_PER_UNIT", "{ 88.888889, 88.888889, 400, 92.61898734177215189873 }")
            thisMarlin.set_c("DEFAULT_MAX_FEEDRATE", "{ 200, 200, 5, 25 }")
            thisMarlin.set_c("DEFAULT_MAX_ACCELERATION", "{ 2000, 2000, 200, 10000 }")
            thisMarlin.set_c("E1_DRIVER_TYPE", None)
            thisMarlin.driver_names.remove("E1_DRIVER_TYPE")
            thisMarlin.set_c("TEMP_SENSOR_1", None)
        elif nozzles == 2:
            pass
        else:
            raise NotImplementedError(
                "Only --nozzles 1 or --nozzles 2 is implemented."
            )
        zmax_answer = options.get('zmax')
        if zmax_answer is not True:
            while True:
                zmax_answer = input(
                    'Did you install a ZMAX sensor'
                    ' (at a custom-drilled location at the bottom) (y/n)? '
                )
                zmax_answer = zmax_answer.lower().strip()
                if zmax_answer in ["y", "yes"]:
                    zmax_answer = True
                    break
                elif zmax_answer in ["n", "no"]:
                    zmax_answer = False
                    break
                else:
                    echo0("Specify y/yes or n/no.")
        if zmax_answer is True:
            thisMarlin.set_multiple_c(LOW_CUSTOM_ZMAX_VALUES)

        # Always invert endstops that make a connection when triggered.
        #   (already done in BLTouch config further up--see
        #   (X|Y|Z)_(MIN|MAX)_ENDSTOP_INVERTING).
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
        # tft_v = ""
        if tft_ans == "y":
            thisMarlin.set_multiple_c(
                BTT_TFT_C_VALUES,
                comment_d=BTT_TFT_C_COMMENTS,
            )
            thisMarlin.set_multiple_c_a(
                BTT_TFT_C_VALUES,
                comment_d=BTT_TFT_C_COMMENTS,
            )

        runout = input("Use a filament runout sensor (y/n)? ").lower()
        if runout not in ['y', 'n']:
            raise ValueError("You must choose y/n for yes/no")
        runout_v = ""
        if runout == "n":
            runout_v = None
        thisMarlin.set_c('FILAMENT_RUNOUT_SENSOR', runout_v)
    else:
        usage()
        raise NotImplementedError('machine="{}"'.format(machine))
    # default_s = driver_types[0]
    if driver_type is None:
        echo0("Please specify --driver-type such as one of {} and try again."
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

    thisMarlin.save_changes()  # Only saves if necessary.

    cmd_parts = ["meld", thisMarlin.m_path, dstMarlin.m_path]
    print("")
    print("# You must use one of the following manual methods for safety.")
    print("# Get a patch (for stock headers) using cache:")
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

    print("# Get a patch for the destination using cache:")
    print(shlex.join([
        "diff",
        "-u",
        thisMarlin.c_path,
        dstMarlin.c_path,
    ]))
    print(shlex.join([
        "diff",
        "-u",
        thisMarlin.c_a_path,
        dstMarlin.c_a_path,
    ]))

    try_merge_programs = ["diffuse", "meldq", "meld", "tkdiff"]
    # ^ meldq is a quiet meld script from github.com/poikilos/linux-preinstall
    dir_merge_programs = ["meldq", "meld", "tkdiff"]
    default_merge_program = "meld"
    print("# Manually merge the changes to complete the process using")
    print("#   any merging program")
    # print("#   (specify the file such as Configuration.h")
    # print("#   if not one of {}):".format(dir_merge_programs))
    show_merge_programs = []
    for merge in try_merge_programs:
        program_path = which(merge)
        if program_path is not None:
            show_merge_programs.append(merge)
    if len(show_merge_programs) == 0:
        show_merge_programs.append(default_merge_program)
        print("# (Install {} or any of {} then)"
              "".format(show_merge_programs[0], try_merge_programs))
    for program in show_merge_programs:
        if program not in dir_merge_programs:
            new_commands = MarlinInfo.transfer_paths_in(cmd_parts)
            for new_parts in new_commands:
                print(shlex.join([program]+new_parts[1:]))
        else:
            print(shlex.join([program]+cmd_parts[1:]))
    print('# Or if you\'re sure "{}" matches "{}"'
          ' then you could do something like:')
    print('rsync -rt "{}/" "{}"'.format(thisMarlin.m_path, dstMarlin.m_path))
    # See <https://stackoverflow.com/a/3516106/4541104>
    proc = Popen(cmd_parts, shell=False,
                 stdin=None, stdout=None, stderr=None, close_fds=True)
    # ^ shell=True made the output stop spamming the console.
    # ^ close_fds: make parent process' file handles inaccessible to child
    print(POST_MERGE_DOC_FMT.format(
        marlin_path=dstMarlin.m_path,
    ))
    if zmax_answer is True:
        print()
        print("All of the sundry settings related to the --zmax option"
              " have been set to prevent grinding the z-axis follower,"
              " as long as you:")
        print("* Followed the directions in the readme for placing the"
              " z axis endstop (or change the Z_MAX_POS accordingly).")
        print("* Run UBL (Menu, Movement, Bed Level, UBL, Start)"
              " and when it finishes save to EEPROM"
              " (*before doing any Home command*)")
        print("  * If it has a stop error, see bed leveling"
              " in the manual in the documentation folder of marlininfo.")
        print("* Some/all of the actions above may not be necessary in"
              " Marlin bugfix-2.1.x if you have commit 21971f2 which"
              " fixes [Mesh bed leveling doesn't handle Z_MAX homing properly]"
              "(https://github.com/MarlinFirmware/Marlin/issues/10390)"
              " and the steps still don't seem to fix the issue in"
              " previous versions including bugfix-2.0.x anyway unless"
              " you completely prevent the bed from sliding down"
              " every time the motors turn off and you ensure that the"
              " nozzle is all the way to the bed each time you turn the"
              " printer on so it thinks that is 0.")

    if len(thisMarlin._not_changed) > 0:
        print()
        print('The following settings were not changed in "{}"'
              ' (not found or already set--you should check them before'
              ' merging with "{}"):'
              ''.format(thisMarlin.m_path, dstMarlin.m_path))
        # for line in thisMarlin._not_changed:
        for info in thisMarlin._not_changed:
            why = None
            newV = info._v
            # newLineI = info._i
            newName = info._n
            oldV, oldLineN, oldName, oldErr = srcMarlin.get_cached_rel(
                info._n,
                info._path,
            )
            relpath = srcMarlin.get_relative(info._path)

            if oldLineN > -1:
                oldLineI = oldLineN - 1
                old_v_hr = c_val_hr(oldV)
                new_v_hr = c_val_hr(newV)
                if old_v_hr == new_v_hr:
                    '''
                    why = ('// (already {} in {}/{})'
                           ''.format(new_v_hr, thisMarlin.mm_path, relpath))
                    '''
                    pass
                else:
                    why = ('// (why is UNKNOWN; {} != {} ::'
                           ' {}/{} != {}/{})'
                           ''.format(old_v_hr, new_v_hr,
                                     srcMarlin.mm_path, relpath,
                                     thisMarlin.mm_path, relpath))
                line = srcMarlin.get_line(oldLineI, info._path)
            else:
                why = ('// not in {} ({}/{})'
                       ''.format(info._path, srcMarlin.mm_path, relpath))
                # ^ It must not be in srcMarlin, since thisMarlin is
                #   a changed copy of srcMarlin.
                line = "{}".format(newName)
            if why is not None:
                print('`{}` {}'.format(line.strip(), why))
        print()
    else:
        print('All settings were applied but only to "{}".'
              ''.format(thisMarlin.m_path))

    return 0


if __name__ == "__main__":
    sys.exit(main())
