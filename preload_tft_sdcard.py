#!/usr/bin/env python3
'''
This script places R2X_14T settings in the current directory. Ensure
you are in the SD card directory first!

Usage:
got.py {sd_card_path}
# where {sd_card_path} is the folder path of the SD card.
'''


import os
import sys
import platform
import subprocess
import shutil

if platform.system() == "Windows":
    HOME = os.environ['USERPROFILE']
    USER = os.environ['USERNAME']
else:
    HOME = os.environ['HOME']
    USER = os.environ['USER']

from marlininfo import (
    echo0,
)

from marlininfo.getrepo import (
    get_or_pull,
    repo_flag_sub,
)

MODULE_DIR = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = os.path.dirname(MODULE_DIR)
REPOS_DIR = os.path.dirname(REPO_DIR)
if os.path.isfile(os.path.join(REPOS_DIR, "hierosoft", "hierosoft",
                  "__init.py__")):
    sys.path.insert(0, os.path.join(REPOS_DIR), "hierosoft")

from hierosoft.morebytes import (
    ByteConf,
)

def echo0(*args):
    print(*args, file=sys.stderr)


def usage(sd_card_path="/mnt/sdf"):
    echo0(__doc__.format(sd_card_path=sd_card_path))



def change_tft_conf_for_r2x(config_path, klipper=True,
                            X_BED_SIZE=242, Y_BED_SIZE=153):
    echo0('[change_tft_conf_for_r2x] Editing "{}"...'
          ''.format(os.path.basename(config_path)))
    conf = ByteConf()
    conf.load(config_path)
    conf.set("status_screen", "1")
    if not klipper:
        conf.set("emulated_m600", "0")  # 0: Only load/retract using *Marlin* & only if there!
    # conf.set("default_mode", "0")  # 0 Marlin (such as for Klipper), 1 Touch
    # ^ apparently touch ("12864 mode") works in Klipper now
    #   (See https://www.reddit.com/r/klippers/comments/prf3fm/
    #   comment/hdkk7a8/?utm_source=share&utm_medium=web2x&context=3)
    #   so keep default_mode:1 (the default default_mode...)
    # min_temp:180
    conf.set("min_temp", "170")
    # M115_GEOMETRY_REPORT supercedes manual settings:
    # size_min:X0 Y0 Z0
    # size_max:X235 Y235 Z250
    # TODO: change from default z_speed:S500 N1000 F2000
    if klipper:
        conf.set("M27_always_active", "0")  # Keep polling M27 if not printing
        conf.set("auto_load_leveling", "0")
    else:
        conf.set("auto_load_leveling", "1")  # 0 is default
        conf.set("M27_always_active", "1") # 1 is default
    conf.set("pause_retract", "R6.0 P7.0")  # P: resume purge length
    # pause_pos:X10.0 Y10.0
    conf.set("pause_pos", "X{}.0 Y{}.0".format(int(X_BED_SIZE-10), int(Y_BED_SIZE-10)))
    # pause_z_raise:10.0
    # TODO: change default pause_feedrate:XY6000 Z6000 E600
    # TODO: check the following defaults:
    # level_edge_distance:20
    # level_z_pos:0.2
    # level_z_raise:10.0
    # level_feedrate:XY6000 Z6000
    # inverted_axis:X0 Y0 Z0 LY0
    # probing_z_raise:20.0
    # TODO: For Voron, change from default z_steppers_alignment:0
    conf.set("M27_always_active", "1")
    # preheat_name_6:NYLON
    # preheat_temp_6:T250 B90
    conf.set("preheat_name_6", "NYLON")
    conf.set("preheat_temp_6", "T250 B90")
    # TODO: change defaults according to a boolean setting:
    # fil_runout:0
    # fil_runout_inverted:1
    # fil_runout_nc:1
    # fil_runout_noise_threshold:100
    # TODO: change default according to printer:
    # fil_runout_distance:7
    # start_gcode_enabled:0
    # end_gcode_enabled:0
    # cancel_gcode_enabled:0
    # start_gcode:G28 XY R20\n
    # end_gcode:M104 S0\nM140 S0\nM107\nM18\n
    # cancel_gcode:M104 S0\nM140 S0\nG28 XY R10\nM107\nM18\n
    conf.set("pl_recovery", "0")
    # ^ Why 0: See [3D Printer Blobs: a mysterious problem you won't
    #   guess how to fix](https://www.youtube.com/watch?v=ZM1MYbsC5Aw)!
    # TODO: Set the following (I forget to what was useful & missing...
    #   probe offset??):
    # custom_label_8:custom8
    # custom_gcode_8:M105\n
    # custom_label_9:custom9
    # custom_gcode_9:M105\n
    conf.save()


def preload_card(sd_card_path,
        firmware_sub="Copy to SD Card root directory to update",
        bin_name="BIGTREE_GD_TFT35_V3.0.27.x.bin",
        theme="THEME_Unified Menu Material theme",
        languages_sub="Language Packs",
        language_pack="language_en.ini", # doesn't matter, see docstring
        theme_model_sub="TFT35", config="config.ini",
        klipper=True,
    ):
    '''
    Load the latest firmware onto the SD card.

    Keyword arguments:
    bin_name -- The name of the bin file in firmware_sub.
    firmware_sub -- The subdirectory of the BIGTREETECH-TouchScreenFirmware
        repo that contains bin_name.
    theme -- The preferred theme subdirectory in firmware_sub.
        Set to None to skip!
    theme_model_sub -- The sub-sub-subdirectory (name not path) under
        theme that contains the correct bmp and font directories for the
        device.
    languages_sub -- The languages directory name (not path) under
        firmware_sub. Unused! ...See language_pack.
    language_pack -- doesn't matter apparently, only for 2nd language
        (The TouchScreenFirmware setting "language:0" is English and
        means don't use another).
    config -- The path to the config, otherwise use default named this
        (if not a full path) in firmware_sub.
    klipper -- If True, change certain settings for Klipper, mostly
        try to prevent TFT from sending G-codes to the board.

    Raises:
    FileNotFoundError -- If any of the specified location does not
        exist.
    '''
    # TODO: non-R2X settings

    echo0("[preload_card] * downloading data for {}".format(sd_card_path))
    if not os.path.exists(sd_card_path):
        usage()
        echo0('Error: "{}" does not exist.'.format(sd_card_path))
        return 1
    if not os.path.isdir(sd_card_path):
        usage()
        echo0('Error: "{}" is not a directory.'.format(sd_card_path))
        return 1
    repos_dir = os.path.join(HOME, "Downloads", "git", "bigtreetech")
    if not os.path.isdir(repos_dir):
        os.makedirs(repos_dir)
    repo_dir = os.path.join(repos_dir, "BIGTREETECH-TouchScreenFirmware")
    repo_url = "https://github.com/bigtreetech/BIGTREETECH-TouchScreenFirmware.git"
    code = get_or_pull(repo_url, repo_dir)
    if code != 0:
        echo0("[preload_card] get_or_pull...FAILED (error code {} {})"
              "".format(type(code).__name__, code))
        return code
    echo0("[preload_card] get_or_pull...OK")

    # Do all sanity checks before copying anything:
    firmware_dir = os.path.join(repo_dir, firmware_sub)
    bin_path = os.path.join(firmware_dir, bin_name)
    if not os.path.isfile(bin_path):
        raise FileNotFoundError('"{}" does not exist.'.format(bin_path))
    echo0('[preload_card] * using "{}"'.format(bin_name))
    theme_path = None
    dst_model_sub_path = None
    if theme is not None:
        theme_path = os.path.join(firmware_dir, theme, theme_model_sub)
        if not os.path.isdir(theme_path):
            raise FileNotFoundError('"{}" does not exist.'.format(theme_path))
        echo0('[preload_card] * using "{}"'.format(theme))
        dst_model_sub_path = os.path.join(sd_card_path, theme_model_sub)

    '''
    languages_path = os.path.join(firmware_dir, languages_sub)
    if not os.path.isdir(languages_path):
        raise FileNotFoundError('"{}" does not exist.'.format(languages_path))
    language_path = os.path.join(languages_path, language_pack)
    if not os.path.isfile(language_path):
        raise FileNotFoundError('"{}" does not exist.'.format(language_path))
    '''
    config_path = config
    if not os.path.isfile(config):
        config_path = os.path.join(firmware_dir, config)
        if not os.path.isfile(config_path):
            raise FileNotFoundError(
                'neither "{}" nor "{}" exists.'
                ''.format(config, config_path)
            )

    # Copy everything (except theme_path if caller set theme to None):
    # ^ # must be the correctly-named sub (such as /mnt/SDCARD/TFT35)!
    if theme_path is not None:
        parent = os.path.dirname(theme_path)
        echo0('[preload_card] Copying "{}/{}"...'
              ''.format(os.path.basename(parent), os.path.basename(theme_path)))
        # distutils.dir_util.copy_tree
        shutil.copytree(
            theme_path,
            dst_model_sub_path,
            dirs_exist_ok=True,  # Overwrite instead of FileExistsError
        )
    '''
    shutil.copy(language_path, os.path.join(sd_card_path, language_pack)
    '''
    dst_config_path = os.path.join(sd_card_path, "config.ini")
    echo0('[preload_card] Copying "{}"...'
          ''.format(os.path.basename(bin_path)))
    shutil.copy(config_path, dst_config_path)
    klipper = False

    change_tft_conf_for_r2x(
        dst_config_path,
        klipper=klipper,
    )

    echo0(
        'Saved "{}" (to compare, run `meld "{}" "{}"` if meld is in your path)'
        ''.format(
            os.path.basename(dst_config_path),
            config_path,
            dst_config_path,
        )
    )


def main():
    # if len(sys.argv) < 2:
    #     usage(sd_card_path=os.getcwd())
    # sd_card_path = sys.argv[1]
    sd_card_path = os.getcwd()
    parent = os.path.dirname(sd_card_path)
    oops_sub = repo_flag_sub(parent)
    error = None
    if oops_sub is not None:
        error = '{} was detected in "{}"'.format(oops_sub, parent)
    else:
        # Check if grandparent is repo in case running from module dir.
        parent = os.path.dirname(parent)
        oops_sub = repo_flag_sub(parent)
        error = None
        if oops_sub is not None:
            error = '{} was detected in "{}"'.format(oops_sub, parent)

    if error is not None:
        sd_card_path = None
        try:
            import psutil
            sdiskparts = list(psutil.disk_partitions(all=False))
            # all=True for network as well
            partitions = []
            for diskpart in sdiskparts:
                '''
                ^ Each item is like:
                sdiskpart(device='/dev/sdd1',
                mountpoint='/run/media/owner/MAKERBOT2B',
                fstype='vfat',
                opts='rw,nosuid,nodev,relatime,uid=1000,gid=1000,
                fmask=0022,dmask=0022,codepage=437,iocharset=ascii,
                shortname=mixed,showexec,utf8,flush,errors=remount-ro',
                maxfile=1530, maxpath=4096)
                '''
                partitions.append(diskpart.mountpoint)

        except ImportError:
            drives_root = "/run/media/{}".format(USER)
            error += ("; drives can be detected better with psutil"
                      " (only {} was checked)".format(drives_root))
            subs = list(os.listdir(drives_root))
            partitions = [os.path.join(drives_root, sub) for sub in subs]
        partition_count = len(partitions)
        for sub_path in partitions:
            parent, sub = os.path.split(sub_path)
            if not os.path.isdir(sub_path):
                continue
            if os.path.isfile(os.path.join(sub_path, "got.py")):
                error = None
                sd_card_path = sub_path
                break
            if sd_card_path is None:
                error += "; no got.py in {}".format(sub_path)
        if partition_count < 1:
            error += "; no partitions were found"
    if sd_card_path is not None:
        parent = sd_card_path
        oops_sub = repo_flag_sub(sd_card_path)
        if oops_sub is None:
            parent = os.path.dirname(sd_card_path)
            oops_sub = repo_flag_sub(parent)
        if oops_sub is not None:
            error = '{} was detected in "{}"'.format(oops_sub, parent)
    if error is None:
        if sd_card_path is None:
            raise NotImplementedError(
                "sd_card_path wasn't set but there was no error."
            )
    if error is not None:
        usage()

        echo0('Error: You appear to be running from the repo'
              ' ({})'
              ' but should run from an SD card or insert one with'
              ' got.py.'
              ''.format(error))
        return 1

    return preload_card(sd_card_path, theme=None)


if __name__ == "__main__":
    sys.exit(main())
