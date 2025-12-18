@echo off
echo ========================================
echo IDURAR ERP CRM - Frontend Tests
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Installing dependencies...
pip install selenium webdriver-manager

echo.
echo Running frontend tests...
echo.

python frontend_tests.py

echo.
echo ========================================
echo Tests completed!
echo Check screenshots folder for results
echo ========================================
pause
