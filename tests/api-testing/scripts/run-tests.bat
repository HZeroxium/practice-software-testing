@echo off
REM API Testing Runner for Windows
REM This script runs the API tests using Python and Newman

echo ========================================
echo API Testing Runner - The Toolshop
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if Newman is installed
newman --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Newman is not installed or not in PATH
    echo Please install Newman: npm install -g newman
    pause
    exit /b 1
)

echo Dependencies check passed!
echo.

REM Set the base URL (can be modified as needed)
set BASE_URL=http://localhost:8000/api

echo Starting API tests with base URL: %BASE_URL%
echo.

REM Run the tests
python scripts/run-api-tests.py --base-url %BASE_URL%

echo.
echo Test execution completed!
echo Check the reports directory for detailed results.
echo.
pause
