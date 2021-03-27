SETLOCAL ENABLEDELAYEDEXPANSION

SET SUMMARY_FILE=C:\Users\AFEIAS\stock_py\combined_dataset\2020\2020_combined_complete.csv
IF EXIST "%SUMMARY_FILE%" (DEL "%SUMMARY_FILE%")
CD C:\Users\AFEIAS\stock_py\dataset\2020\

SET /A LINE_COUNT=1

FOR /F "usebackq tokens=*" %%f IN (`DIR /S /B *.csv`) DO (
    FOR /F "usebackq tokens=*" %%s IN (`TYPE "%%~f"`) DO (
        ECHO %%s >>"%SUMMARY_FILE%"  
        SET /A LINE_COUNT=!LINE_COUNT! + 1
    )
)
EXIT /B 0
