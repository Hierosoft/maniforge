@ECHO OFF
SET SRC_BRANCH=.\Marlin-r2x_14t
SET SRC_BRANCH_MARLIN=.\Marlin-r2x_14t\Marlin
SET DST_BRANCH=..\Marlin
REM IF EXIST ..\..\git\Marlin SET DST_BRANCH=..\..\git\Marlin
REM ^ Done in pushconfig.bat
CALL utilities/pushconfig.bat
