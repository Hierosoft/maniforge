REM call this after setting SRC_BRANCH and DST_BRANCH (See examples in "..", the main r2x_14t repo directory).
IF EXIST %SRC_BRANCH%\Configuration.h SET SRC_BRANCH_MARLIN=%SRC_BRANCH%
REM ^ Handle flat directory structures like the Configuration examples in MarlinFirmware's Configurations repo's example directories.
IF EXIST ..\..\git\Marlin\Marlin\Configuration.h SET DST_BRANCH=..\..\git\Marlin
ECHO INFO: %DST_BRANCH% will be used since Marlin\Configuration.h was detected there.
IF NOT EXIST %DST_BRANCH%\Marlin\Configuration.h ECHO Error: There is no %DST_BRANCH%\Marlin\Configuration.h to replace.
IF NOT EXIST %DST_BRANCH%\Marlin\Configuration.h GOTO BAD_DST
IF NOT EXIST %DST_BRANCH%\Marlin\Configuration_adv.h ECHO Error: There is no %DST_BRANCH%\Marlin\Configuration_adv.h replace.
IF NOT EXIST %DST_BRANCH%\Marlin\Configuration_adv.h GOTO BAD_DST
IF NOT EXIST %DST_BRANCH%\platformio.ini ECHO Error: There is no %DST_BRANCH%\platformio.ini to replace.
IF NOT EXIST %DST_BRANCH%\platformio.ini GOTO BAD_DST
IF NOT EXIST %SRC_BRANCH_MARLIN%\Configuration.h ECHO Error: There is no %SRC_BRANCH_MARLIN%\Configuration.h
IF NOT EXIST %SRC_BRANCH_MARLIN%\Configuration.h GOTO BAD_SRC
IF NOT EXIST %SRC_BRANCH_MARLIN%\Configuration_adv.h ECHO Error: There is no %SRC_BRANCH_MARLIN%\Configuration_adv.h
IF NOT EXIST %SRC_BRANCH_MARLIN%\Configuration_adv.h GOTO BAD_SRC
copy %SRC_BRANCH_MARLIN%\Configuration.h %DST_BRANCH%\Marlin\
copy %SRC_BRANCH_MARLIN%\Configuration_adv.h %DST_BRANCH%\Marlin\
copy %SRC_BRANCH%\platformio.ini %DST_BRANCH%\
GOTO ENDSILENT

:BAD_DST
echo The directory %DST_BRANCH% doesn't seem to be the Marlin repo containing the Marlin subdirectory of the same name. First clone according to readme.md.

:BAD_SRC

:ENDSILENT
