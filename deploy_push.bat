@echo off
setlocal

REM === Variables ===
set SCRIPT=deploy_push.py

REM === Check for Python ===
where python >nul 2>nul
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.x first.
    exit /b 1
)

REM === Optional: create venv ===
if not exist "venv\" (
    python -m venv venv
)

call venv\Scripts\activate.bat

REM === Launch the script ===
python %SCRIPT% %*

endlocal