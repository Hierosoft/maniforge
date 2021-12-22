@echo off
SET DST_BRANCH=..\Marlin
IF EXIST ..\..\git\Marlin\Marlin\Configuration.h SET DST_BRANCH=..\..\git\Marlin
ECHO INFO: %DST_BRANCH% will be used since Marlin\Configuration.h was detected there.
IF NOT EXIST %DST_BRANCH%\Marlin\Configuration.h GOTO ENDBAD
copy Marlin-r2x_14t\Marlin\Configuration.h %DST_BRANCH%\Marlin\
IF NOT EXIST %DST_BRANCH%\Marlin\Configuration_adv.h GOTO ENDBAD
copy Marlin-r2x_14t\Marlin\Configuration_adv.h %DST_BRANCH%\Marlin\
IF NOT EXIST %DST_BRANCH%\platformio.ini GOTO ENDBAD
copy Marlin-r2x_14t\platformio.ini %DST_BRANCH%\
GOTO ENDSILENT

:ENDBAD
echo The directory %DST_BRANCH% doesn't seem to be the Marlin repo containing the Marlin subdirectory of the same name. First clone according to readme.md.

:ENDSILENT
