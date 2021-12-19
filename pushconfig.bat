@echo off
SET SRC_MARLIN=..\Marlin
IF EXIST ..\..\git\Marlin\Marlin\Configuration.h SET SRC_MARLIN=..\..\git\Marlin
ECHO INFO: %SRC_MARLIN% will be used since Marlin\Configuration.h was detected there.
IF NOT EXIST %SRC_MARLIN%\Marlin\Configuration.h GOTO ENDBAD
copy Marlin-r2x_14t\Marlin\Configuration.h %SRC_MARLIN%\Marlin\
IF NOT EXIST %SRC_MARLIN%\Marlin\Configuration_adv.h GOTO ENDBAD
copy Marlin-r2x_14t\Marlin\Configuration_adv.h %SRC_MARLIN%\Marlin\
IF NOT EXIST %SRC_MARLIN%\platformio.ini GOTO ENDBAD
copy Marlin-r2x_14t\platformio.ini %SRC_MARLIN%\
GOTO ENDSILENT

:ENDBAD
echo The directory %SRC_MARLIN% doesn't seem to be the Marlin repo containing the Marlin subdirectory of the same name. First clone according to readme.md.

:ENDSILENT
