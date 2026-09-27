@echo off
REM Installs this project's Python requirements and rustfmt (if rustup is available).
setlocal

set "SCRIPT_DIR=%~dp0"

echo Installing Python requirements...
pip install -r "%SCRIPT_DIR%..\requirements.txt"

echo.
where rustup >nul 2>&1
if %errorlevel%==0 (
    echo Installing rustfmt via rustup...
    rustup component add rustfmt
) else (
    where rustfmt >nul 2>&1
    if %errorlevel%==0 (
        echo rustfmt already installed, skipping.
    ) else (
        echo rustup not found, skipping rustfmt.
        echo Install Rust via https://rustup.rs, then run: rustup component add rustfmt
    )
)

endlocal
