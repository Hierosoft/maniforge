IF NOT EXIST deploy-marlin GOTO DOTDOT
python deploy-marlin %*
:DOTDOT:
python ..\deploy-marlin %*
