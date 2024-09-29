@echo off
REM Check if pip is installed
python -m pip --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo Python is not installed or pip is not available. Please install Python and ensure it is added to your PATH.
    exit /b
)

REM Install required packages
echo Installing required packages...
pip install uvicorn fastapi requests

REM Check if the packages were installed successfully
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install some packages. Please check the output for errors.
    exit /b
)

echo All packages installed successfully!
pause
