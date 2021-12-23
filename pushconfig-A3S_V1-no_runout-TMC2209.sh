#!/bin/bash
SRC_BRANCH=./Marlin-A3S_V1-no_runout-TMC2209
DST_BRANCH=../Marlin
if [ ! -d "$DST_BRANCH" ]; then
    TRY_DST="$HOME/Downloads/git/MarlinFirmware/Marlin"
    if [ -d "$TRY_DST" ]; then
        DST_BRANCH="$TRY_DST"
    fi
fi
# SRC_BRANCH="$HOME/git/Configurations/config/examples/JGAurora/A3S_V1"
# if [ ! -d "$SRC_BRANCH" ]; then
#     echo "Error: There is no \"$SRC_BRANCH\". If the Poikilos A3S_V1 configuration isn't pulled upstream yet, ensure you cloned the Poikilos' fork of the MarlinFirmware Configurations repo and that you have, in that directory, run \"git switch bugfix-2.0.x-A3S_MK1\"."
#     exit 1
# fi
. utilities/pushconfig.sh
