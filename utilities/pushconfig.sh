#!/bin/bash
# Call this after setting SRC_BRANCH and DST_BRANCH (See examples in "..", the main r2x_14t repo directory).

if [ -z "$SRC_BRANCH" ]; then
    echo "Error: SRC_BRANCH is not set."
    exit 1
fi

if [ -z "$DST_BRANCH" ]; then
    echo "Error: DST_BRANCH is not set."
    exit 1
fi


endbad(){
cat <<END
 The directory $DST_BRANCH doesn't seem to be the Marlin repo containing the Marlin subdirectory of the same name. First clone according to readme.md.
END
    exit 1
}

SRC_BRANCH_MARLIN="$SRC_BRANCH/Marlin"
if [ -f "$SRC_BRANCH/Configuration.h" ]; then
    SRC_BRANCH_MARLIN="$SRC_BRANCH"
fi
# ^ Handle flat directory structures like the Configuration examples in MarlinFirmware's Configurations repo's example directories.
if [ -f ../../git/Marlin/Marlin/Configuration.h ]; then
    DST_BRANCH="../../git/Marlin"
    echo "INFO: $DST_BRANCH will be used since Marlin/Configuration.h was detected there.";
fi
if [ ! -f "$DST_BRANCH/Marlin/Configuration.h" ]; then
    echo "Error: There is no $DST_BRANCH/Marlin/Configuration.h to replace."
    endbad
fi
if [ ! -f "$DST_BRANCH/Marlin/Configuration_adv.h" ]; then
    echo "Error: There is no $DST_BRANCH/Marlin/Configuration_adv.h replace."
    endbad
fi
if [ ! -f "$DST_BRANCH/platformio.ini" ]; then
    echo "Error: There is no $DST_BRANCH/platformio.ini to replace."
    endbad
fi

if [ ! -f "$SRC_BRANCH_MARLIN/Configuration.h" ]; then
    echo "Error: There is no $SRC_BRANCH_MARLIN/Configuration.h."
    exit 1
fi
if [ ! -f "$SRC_BRANCH_MARLIN/Configuration_adv.h" ]; then
    echo "Error: There is no $SRC_BRANCH_MARLIN/Configuration_adv.h."
    exit 1
fi

echo "* patching $DST_BRANCH..."

cp -v "$SRC_BRANCH_MARLIN/Configuration.h" "$DST_BRANCH/Marlin/"
if [ $? -ne 0 ]; then exit 1; fi
cp -v "$SRC_BRANCH_MARLIN/Configuration_adv.h" "$DST_BRANCH/Marlin/"
if [ $? -ne 0 ]; then exit 1; fi
if [ -f "$SRC_BRANCH/platformio.ini" ]; then
    cp -v "$SRC_BRANCH/platformio.ini" "$DST_BRANCH/"
    if [ $? -ne 0 ]; then exit 1; fi
fi
echo "Done."
echo
exit 0
