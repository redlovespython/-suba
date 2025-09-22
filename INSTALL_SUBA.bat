@echo off
title 'suba Installer
color 0A

echo ==================================================
echo              'suba ONE-CLICK INSTALLER
echo       Simple Utility for Broadcasting AIMP  
echo                   made by red.py
echo ==================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo.
    echo Please install Python first:
    echo 1. Go to https://python.org/downloads/
    echo 2. Download Python 3.8 or newer
    echo 3. IMPORTANT: Check "Add Python to PATH" during installation
    echo 4. Run this installer again
    echo.
    pause
    exit /b
)

echo [OK] Python is installed
echo.

:: Check if setup files exist
if not exist "suba_setup.py" (
    echo [ERROR] suba_setup.py not found
    echo Make sure all files are in the same folder
    echo.
    pause
    exit /b
)

if not exist "suba.py" (
    echo [ERROR] suba.py not found
    echo Make sure all files are in the same folder
    echo.
    pause
    exit /b
)

:: Run the setup script
echo Starting 'suba Setup Wizard...
echo.
timeout /t 2 /nobreak >nul

python suba_setup.py

if %errorlevel% neq 0 (
    echo.
    echo ==================================================
    echo [ERROR] Setup failed
    echo ==================================================
    pause
    exit /b
)

exit
