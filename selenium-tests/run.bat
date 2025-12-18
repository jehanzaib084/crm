@echo off
echo ========================================
echo IDURAR ERP CRM - Selenium Tests
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements_simple.txt

echo.
echo Running tests...
echo.

python simple_test.py

echo.
echo ========================================
echo Tests completed!
echo Check screenshots folder for results
echo ========================================
pause
