@echo off
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"


set "NOW=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"
set "PROJ_ROOT=%~dp0\..\..\..\"
set "DATA_ROOT=c:\dev\data\usup_reg\raw\uci\concrete"
set "WORK_ROOT=c:\dev\data\usup_reg\work"

echo "Running experiments on concrete data"

mkdir "%WORK_ROOT%/baseline/lr/concrete/%NOW%"
.\baseline\lr\concrete.bat > "%WORK_ROOT%/baseline/lr/concrete/%NOW%/concrete_baseline.log" 2>&1