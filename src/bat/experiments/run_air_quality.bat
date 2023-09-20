@echo off
for /f "tokens=2 delims==" %%a in ('wmic OS Get localdatetime /value') do set "dt=%%a"
set "YY=%dt:~2,2%" & set "YYYY=%dt:~0,4%" & set "MM=%dt:~4,2%" & set "DD=%dt:~6,2%"
set "HH=%dt:~8,2%" & set "Min=%dt:~10,2%" & set "Sec=%dt:~12,2%"


set "NOW=%YYYY%-%MM%-%DD%_%HH%-%Min%-%Sec%"
set "PROJ_ROOT=%~dp0\..\..\..\"
set "DATA_ROOT=c:\dev\data\usup_reg\raw\uci\air_quality"
set "WORK_ROOT=c:\dev\data\usup_reg\work"
set "CWD=%~dp0"


echo "Running experiments on air_quality data COGT prediction"

cd "%CWD%"
mkdir "%WORK_ROOT%\baseline\lr\air_quality_COGT\%NOW%"
call .\baseline\lr\air_quality_COGT.bat > "%WORK_ROOT%\baseline\lr\air_quality_COGT\%NOW%\air_quality_COGT_baseline.log" 2>&1

cd "%CWD%"
mkdir "%WORK_ROOT%\adwin_with_z1_z2\lr\air_quality_COGT\%NOW%"
call .\adwin_with_z1_z2\lr\air_quality_COGT.bat > "%WORK_ROOT%\adwin_with_z1_z2\lr\air_quality_COGT\%NOW%\air_quality_COGT_adwin_with_z1_z2.log" 2>&1

cd "%CWD%"
mkdir "%WORK_ROOT%\z1_z2_only\lr\air_quality_COGT\%NOW%"
call .\z1_z2_only\lr\air_quality_COGT.bat > "%WORK_ROOT%\z1_z2_only\lr\air_quality_COGT\%NOW%\air_quality_COGT_z1_z2_only.log" 2>&1



rem echo "Running experiments on air_quality data NO2 prediction"

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\baseline\lr\air_quality_NO2\%NOW%"
rem call .\baseline\lr\air_quality_NO2.bat > "%WORK_ROOT%\baseline\lr\air_quality_NO2\%NOW%\air_quality_NO2_baseline.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\adwin_with_z1_z2\lr\air_quality_NO2\%NOW%"
rem call .\adwin_with_z1_z2\lr\air_quality_NO2.bat > "%WORK_ROOT%\adwin_with_z1_z2\lr\air_quality_NO2\%NOW%\air_quality_NO2_adwin_with_z1_z2.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\z1_z2_only\lr\air_quality_NO2\%NOW%"
rem call .\z1_z2_only\lr\air_quality_NO2.bat > "%WORK_ROOT%\z1_z2_only\lr\air_quality_NO2\%NOW%\air_quality_NO2_z1_z2_only.log" 2>&1



rem echo "Running experiments on air_quality data NMHCGT prediction"

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\baseline\lr\air_quality_NMHCGT\%NOW%"
rem call .\baseline\lr\air_quality_NMHCGT.bat > "%WORK_ROOT%\baseline\lr\air_quality_NMHCGT\%NOW%\air_quality_NMHCGT_baseline.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\adwin_with_z1_z2\lr\air_quality_NMHCGT\%NOW%"
rem call .\adwin_with_z1_z2\lr\air_quality_NMHCGT.bat > "%WORK_ROOT%\adwin_with_z1_z2\lr\air_quality_NMHCGT\%NOW%\air_quality_NMHCGT_adwin_with_z1_z2.log" 2>&1

rem cd "%CWD%"
rem mkdir "%WORK_ROOT%\z1_z2_only\lr\air_quality_NMHCGT\%NOW%"
rem call .\z1_z2_only\lr\air_quality_NMHCGT.bat > "%WORK_ROOT%\z1_z2_only\lr\air_quality_NMHCGT\%NOW%\air_quality_NMHCGT_z1_z2_only.log" 2>&1
