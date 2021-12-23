@ECHO OFF
SET SRC_BRANCH=.\Marlin-A3S_V1-no_runout-TFT24
SET DST_BRANCH=..\Marlin
REM SET SRC_BRANCH=%USERPROFILE%\git\Configurations\config\examples\JGAurora\A3S_V1
REM IF NOT EXIST "%SRC_BRANCH%" ECHO Error: There is no "%SRC_BRANCH%". If the Poikilos A3S_V1 configuration isn't pulled upstream yet, ensure you cloned the Poikilos' fork of the MarlinFirmware Configurations repo and that you have, in that directory, run "git switch bugfix-2.0.x-A3S_MK1".
CALL utilities/pushconfig.bat
