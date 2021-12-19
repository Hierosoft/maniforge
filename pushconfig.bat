IF NOT EXIST ..\Marlin\Marlin\Configuration.h GOTO ENDBAD
copy Marlin-r2x_14t\Marlin\Configuration.h ..\Marlin\Marlin\
IF NOT EXIST ..\Marlin\Marlin\Configuration_adv.h GOTO ENDBAD
copy Marlin-r2x_14t\Marlin\Configuration_adv.h ..\Marlin\Marlin\
IF NOT EXIST ..\Marlin\platformio.ini GOTO ENDBAD
copy Marlin-r2x_14t\platformio.ini ..\Marlin\
GOTO ENDSILENT

:ENDBAD
echo The directory ..\Marlin doesn't seem to be the Marlin repo containing the Marlin subdirectory of the same name. First clone according to readme.md.

:ENDSILENT
