@echo off
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"


set "NOW=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"
set "PROJ_ROOT=%~dp0\..\..\..\"
set "DATA_ROOT=c:\dev\data\usup_reg\raw\uci\turbine"
set "WORK_ROOT=c:\dev\data\usup_reg\work"
set "CWD=%~dp0"

echo "Running experiments on turbine data TEY prediction"

cd "%CWD%"
mkdir "%WORK_ROOT%\baseline\lr\turbine_TEY\%NOW%"
sh .\baseline\lr\turbine_TEY.sh > "%WORK_ROOT%\baseline\lr\turbine_TEY\%NOW%\turbine_TEY.log" 2>&1

cd "%CWD%"
mkdir "%WORK_ROOT%\adwin_with_z1_z2\lr\turbine_TEY\%NOW%"
sh .\adwin_with_z1_z2\lr\turbine_TEY.sh > "%WORK_ROOT%\adwin_with_z1_z2\lr\turbine_TEY\%NOW%\urbine_TEY_adwin_with_z1_z2.log" 2>&1

cd "%CWD%"
mkdir "%WORK_ROOT%\z1_z2_only\lr\turbine_TEY\%NOW%"
sh .\z1_z2_only\lr\turbine_TEY.sh > "%WORK_ROOT%\z1_z2_only\lr\turbine_TEY\%NOW%\turbine_TEY_z1_z2_only.log" 2>&1



rem echo "Running experiments on turbine data CO prediction"

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\baseline\lr\turbine_CO\%NOW%"
rem sh .\baseline\lr\turbine_CO.sh > "%WORK_ROOT%\baseline\lr\turbine_CO\%NOW%\turbine_CO_baseline.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\adwin_with_z1_z2\lr\turbine_CO\%NOW%"
rem sh .\adwin_with_z1_z2\lr\turbine_CO.sh > "%WORK_ROOT%\adwin_with_z1_z2\lr\turbine_CO\%NOW%\turbine_CO_adwin_with_z1_z2.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\z1_z2_only\lr\turbine_CO\%NOW%"
rem sh .\z1_z2_only\lr\turbine_CO.sh > "%WORK_ROOT%\z1_z2_only\lr\turbine_CO\%NOW%\turbine_CO_z1_z2_only.log" 2>&1



rem echo "Running experiments on turbine data NOX prediction"

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\baseline\lr\turbine_NOX\%NOW%"
rem sh .\baseline\lr\turbine_NOX.sh > "%WORK_ROOT%\baseline\lr\turbine_NOX\%NOW%\turbine_NOX_baseline.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\adwin_with_z1_z2\lr\turbine_NOX\%NOW%"
rem sh .\adwin_with_z1_z2\lr\turbine_NOX.sh > "%WORK_ROOT%\adwin_with_z1_z2\lr\turbine_NOX\%NOW%\turbine_NOX_adwin_with_z1_z2.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\z1_z2_only\lr\turbine_NOX\%NOW%"
rem sh .\z1_z2_only\lr\turbine_NOX.sh > "%WORK_ROOT%\z1_z2_only\lr\turbine_NOX\%NOW%\turbine_NOX_z1_z2_only.log" 2>&1
