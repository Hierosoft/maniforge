#!/bin/bash

cd ~/Downloads/git/MarlinFirmware/Marlin && deploy-marlin --machine R2X_14T --T0 1 --zmax

cat >/dev/null <<END
# version-dependent steps:
if [ -d "Marlin-base" ]; then
    cd Marlin-base
fi
# deploy-marlin ~/Downloads/git/MarlinFirmware/Marlin --machine R2X_14T --T0 1 --zmax
cd ~/Downloads/git/MarlinFirmware/Marlin && \
    deploy-marlin --machine R2X_14T --T0 1 --zmax
END
