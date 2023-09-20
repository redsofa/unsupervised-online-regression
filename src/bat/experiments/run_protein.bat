@echo off
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"


set "NOW=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"
set "PROJ_ROOT=%~dp0\..\..\..\"
set "DATA_ROOT=c:\dev\data\usup_reg\raw\uci\concrete"
set "WORK_ROOT=c:\dev\data\usup_reg\work"
set "CWD=%~dp0"

echo "Running experiments on protein data ... "

cd "%CWD%"
mkdir -p "%WORK_ROOT%/baseline/lr/protein/%NOW%" 
call .\baseline\lr\protein.bat > "%WORK_ROOT%/baseline/lr/protein/%NOW%/protein_baseline.log" 2>&1

cd "%CWD%"
mkdir -p "%WORK_ROOT%/z1_z2_only/lr/protein/%NOW%" 
call .\z1_z2_only\lr\protein.bat > "%WORK_ROOT%/z1_z2_only/lr/protein/%NOW&/protein_z1_z2_only.log" 2>&1

cd "%CWD%"
mkdir -p "%WORK_ROOT%/adwin_with_z1_z2/lr/protein/"%NOW%"
call .\adwin_with_z1_z2\lr\protein.bat > "%WORK_ROOT%/adwin_with_z1_z2/lr/protein/%NOW%/protein_adwin_with_z1_z2.log" 2>&1
