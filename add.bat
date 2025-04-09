@echo off
set HOSTS_FILE=%SystemRoot%\System32\drivers\etc\hosts
set ENTRY=127.0.0.1 solar.torn-lotus.com

REM Prüfen, ob der Eintrag schon existiert
findstr /C:"%ENTRY%" "%HOSTS_FILE%" >nul
if %errorlevel%==0 (
    echo Eintrag bereits vorhanden.
) else (
    echo %ENTRY%>>"%HOSTS_FILE%"
    echo Eintrag wurde hinzugefügt.
)
pause
