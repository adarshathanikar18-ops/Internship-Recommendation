@echo off
echo ========================================
echo    InternMatch - Windows Setup Script
echo ========================================
echo.

echo [1/6] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org/downloads
    echo Make sure to check "Add Python to PATH" during installation
    pause
    exit /b 1
)
python --version

echo.
echo [2/6] Creating virtual environment...
python -m venv .venv
if errorlevel 1 (
    echo ERROR: Failed to create virtual environment
    pause
    exit /b 1
)

echo.
echo [3/6] Activating virtual environment...
call .venv\Scripts\activate.bat

echo.
echo [4/6] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [5/6] Setting up database...
python manage_companies.py seed --csv sample_companies.csv
if errorlevel 1 (
    echo ERROR: Failed to create database
    pause
    exit /b 1
)

echo.
echo [6/6] Training ML model...
python model_training.py
if errorlevel 1 (
    echo ERROR: Failed to train model
    pause
    exit /b 1
)

echo.
echo ========================================
echo    Setup Complete! 🎉
echo ========================================
echo.
echo To run the application:
echo 1. Activate virtual environment: .venv\Scripts\activate
echo 2. Run the app: python app.py
echo 3. Open browser: http://127.0.0.1:5000
echo.
echo Press any key to start the application now...
pause >nul

echo.
echo Starting InternMatch...
python app.py