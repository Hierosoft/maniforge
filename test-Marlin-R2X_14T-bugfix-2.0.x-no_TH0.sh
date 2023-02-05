#!/bin/bash
MY_DIR=`realpath .`
me=`basename "$0"`
MY_DIR_NAME=`basename $MY_DIR`
FORMER_PWD="`pwd`"
if [ "$MY_DIR_NAME" != "Marlin-bugfix-2.0.x-base" ]; then
    echo "You are not in $MY_DIR_NAME. Trying cd..."
    cd Marlin-bugfix-2.0.x-base
    code=$?
    if [ $code -ne 0 ]; then
        exit $code
    fi
fi
if [ ! -f "`command -v deploy-marlin`" ]; then
    cd "$FORMER_PWD"
    cat <<END

deploy-marlin is not in the path. Add a symlink to it in one of your bin directories.

END
    if [ -f "deploy-marlin" ]; then
        echo "Example:"
        echo "  ln -s `pwd`/deploy-marlin ~/.local/bin/"
        echo "  # If that bin folder isn't in your PATH,"
        echo "  # add it or replace ~/.local/bin with /usr/local/bin"
    else
        echo "There is no deploy-marlin in `pwd`."
        echo "Run ./$me again from the marlininfo repo root to show an example symlink command."
    fi
    exit 1
fi
# deploy-marlin ~/Downloads/git/MarlinFirmware/Marlin --machine R2X_14T --T0 1 --zmax
deploy-marlin ../Marlin-bugfix-2.0.x-R2X_14T-no_TH0 --machine R2X_14T --T0 1
# --zmax
exit $?
