#!/usr/bin/env python3
"""
This script prepares and SD card to update the TFT24 1.1 firmware.
"""
import os
import sys
import platform
import subprocess
import shutil

profile = None
user = None
if platform.system() == "Windows":
    profile = os.environ['USERPROFILE']
    user = os.environ['%USERNAME%']
else:
    profile = os.environ['HOME']
    user = os.environ['USER']

Downloads = os.path.join(profile, "Downloads")
DownloadsGit = os.path.join(Downloads, "git")

srcRepos = os.path.join(DownloadsGit, "bigtreetech")

srcThemes = [
    "THEME_Hybrid Mono Menu Material theme",
    "THEME_Hybrid Red Menu Material theme",
    "THEME_Rep Rap Firmware Dark theme",
    "THEME_The Round Miracle Menu Material theme",
    "THEME_Unified Menu Material theme",
]


def prerr(msg, newline="\n"):
    sys.stderr.write("{}".format(msg))
    if newline is not None:
        sys.stderr.write(newline)
    sys.stderr.flush()


def buildDrive(srcBttTftRepo, dstSD, displayTypeStr="TFT24_V1.1",
               dataDirName="TFT24", make="BIGTREE"):
    """
    Keyword arguments:
    make -- the display manufacturer
    displayTypeStr -- The make and an underscore will be prepended to
        this to get the unique id of the device to be found in the
        firmware binary's filename. The result should be something like
        "BIGTREE_TFT24_V1.1.27.x.bin".
    """

    if srcBttTftRepo is None:
        raise ValueError("srcBttTftRepo is None.")
    if dstSD is None:
        raise ValueError("dstSD is None.")
    # The following steps are based on the instructions from the readme
    # (in srcBttTftRepo):
    srcTftRoots = os.path.join(srcBttTftRepo, "Copy to SD Card root directory to update")
    idStr = make + "_" + displayTypeStr
    fwName = None
    srcFwPath = None
    for sub in os.listdir(srcTftRoots):
        # Detect the correct one containing idStr such as
        # "BIGTREE_TFT24_V1.1.27.x.bin".
        subPath = os.path.join(srcTftRoots, sub)
        if not os.path.isfile(subPath):
            continue
        if not subPath.endswith(".bin"):
            continue
        if idStr in sub:
            fwName = sub
            srcFwPath = subPath
            break
        # else:
        #     print("  * {} is not in {}".format(idStr, sub))
    if fwName is None:
        raise ValueError("A firmware .bin filename containing {}"
                         " cannot be found in {}."
                         "".format(idStr, srcTftRoots))
    dstFwPath = os.path.join(dstSD, fwName)
    print("* detected a matching firmware binary: {}"
          "".format(srcFwPath))
    if not os.path.isfile(dstFwPath):
        prerr("* copying {}...".format(dstFwPath), newline=None)
        shutil.copy(srcFwPath, dstFwPath)
        prerr("OK")
    else:
        prerr("* keeping existing {}".format(dstFwPath))

    srcConfig = os.path.join(srcTftRoots, "config.ini")
    dstConfig = os.path.join(dstSD, "config.ini")
    prerr("* copying {}...".format(dstConfig), newline=None)
    shutil.copy(srcConfig, dstConfig)
    prerr("OK")

    srcTheme = os.path.join(srcTftRoots, "THEME_The Round Miracle Menu Material theme")
    srcVersionedTheme = os.path.join(srcTheme, dataDirName)
    dstVersionedTheme = os.path.join(dstSD, dataDirName)
    rsyncCmdParts = ["rsync", "-rt", "--delete", srcVersionedTheme+"/", dstVersionedTheme]
    if not os.path.isdir(dstVersionedTheme):
        prerr("* mkdir {}...".format(dstVersionedTheme), newline=None)
        os.mkdir(dstVersionedTheme)
        prerr("OK")

    prerr("* {}...".format(" ".join(rsyncCmdParts)), newline=None)
    subprocess.call(rsyncCmdParts)
    prerr("OK")


if __name__ == "__main__":
    dstSD = None

    drivesPath = os.path.join("/media", user)

    if len(sys.argv) > 1:
        dstSD = sys.argv[1]
        print("* using specified SD card: \"{}\"".format(dstSD))
    else:
        for sub in os.listdir(drivesPath):
            subPath = os.path.join(drivesPath, sub)
            # ^ Such as /media/owner/TFT250000-2
            goodFlags = ["config.ini", "config.ini.CUR"]
            for goodFlag in goodFlags:
                flagPath = os.path.join(subPath, goodFlag)
                if os.path.isfile(flagPath):
                    dstSD = subPath
                    break

    if dstSD is None:
        print("A drive containing config.ini wasn't found in {}."
              " Specify a SD card drive path."
              "".format(drivesPath))
        exit(1)

    srcBttTftRepo = os.path.join(srcRepos, "BIGTREETECH-TouchScreenFirmware")
    buildDrive(srcBttTftRepo, dstSD)

