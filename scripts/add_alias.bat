@echo off
REM cmd has no ~/.bashrc equivalent, so this creates a `format.bat` shim next
REM to this script and adds this folder to your user PATH, so `format file.py`
REM works from any cmd window. Run once, then open a new cmd window.

set "SCRIPT_DIR=%~dp0"
set "REPO_ROOT=%SCRIPT_DIR%.."

set "PYTHON=python"
if exist "%REPO_ROOT%\.venv\Scripts\python.exe" set "PYTHON=%REPO_ROOT%\.venv\Scripts\python.exe"

> "%SCRIPT_DIR%format.bat" (
    echo @echo off
    echo "%PYTHON%" "%REPO_ROOT%\formatter.py" %%*
)
echo Created %SCRIPT_DIR%format.bat

echo %PATH% | find /I "%SCRIPT_DIR%" >nul
if errorlevel 1 (
    REM Note: this permanently overwrites your user PATH via setx. If your
    REM PATH is already very long, setx can silently truncate it -- check
    REM Environment Variables in System Settings if anything looks off after.
    setx PATH "%PATH%;%SCRIPT_DIR%" >nul
    echo Added %SCRIPT_DIR% to your user PATH.
) else (
    echo %SCRIPT_DIR% is already on PATH.
)

echo Open a new cmd window, then run: format file.py
