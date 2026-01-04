@echo off
REM Demo launcher (Windows)
title Secure Channel Demo Launcher

REM Go to repo root
cd /d "%~dp0\.."

REM Pick a free port (5000, 5001, ...)
if "%PORT%"=="" set PORT=5000
:findport
set INUSE=
for /f "tokens=1,2,3,4,5" %%a in ('netstat -ano ^| findstr /r /c:":%PORT% .*LISTENING"') do set INUSE=1
if defined INUSE (
    set /a PORT+=1
    goto findport
)

REM Header
cls
echo.
echo ============================================================
echo    SECURE CHANNEL DEMO - LAUNCHER
echo ============================================================
echo.
echo Starting up... Please wait...
echo.
echo Current folder: %CD%
echo.

REM Python
echo [1/5] Checking Python installation...
python --version 2>nul
if errorlevel 1 (
    cls
    echo.
    echo ============================================================
    echo ERROR: Python not found!
    echo ============================================================
    echo.
    echo Python is not installed or not in your PATH.
    echo.
    echo Please:
    echo 1. Install Python 3.10+ from https://www.python.org/downloads/
    echo 2. During installation, CHECK "Add Python to PATH"
    echo 3. Restart your computer after installation
    echo 4. Try running this script again
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
python --version
echo [OK] Python found!
echo.

REM Files
echo [2/5] Checking project files...
if not exist "requirements.txt" (
    cls
    echo.
    echo ============================================================
    echo ERROR: Project files not found!
    echo ============================================================
    echo.
    echo Cannot find requirements.txt
    echo Current folder: %CD%
    echo.
    echo Make sure you're running this from the project root folder.
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [OK] Project files found!
echo.

REM Dependencies
echo [3/5] Checking dependencies...
REM Use a local venv to avoid system Python permission issues
if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creating virtual environment (.venv)...
    python -m venv .venv
    if errorlevel 1 (
        cls
        echo.
        echo ============================================================
        echo ERROR: Failed to create virtual environment
        echo ============================================================
        echo.
        echo Try installing Python 3.10+ and make sure it's on PATH.
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
)
set "PYTHON=%CD%\.venv\Scripts\python.exe"

%PYTHON% -c "import flask" 2>nul
if errorlevel 1 (
    echo [INFO] Dependencies not installed. Installing now...
    echo This may take a few minutes. Please wait...
    echo.
    %PYTHON% -m pip install --upgrade pip setuptools wheel --quiet
    %PYTHON% -m pip install -r requirements.txt
    if errorlevel 1 (
        cls
        echo.
        echo ============================================================
        echo ERROR: Failed to install dependencies!
        echo ============================================================
        echo.
        echo Please check your internet connection and try again.
        echo Or install manually: pip install -r requirements.txt
        echo.
        echo Press any key to exit...
        pause >nul
        exit /b 1
    )
    echo [OK] Dependencies installed!
) else (
    echo [OK] Dependencies already installed!
)
echo.

REM Backend/frontend
echo [4/5] Checking backend and frontend...
if not exist "backend\app.py" (
    cls
    echo.
    echo ============================================================
    echo ERROR: Backend not found!
    echo ============================================================
    echo.
    echo Cannot find backend\app.py
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
if not exist "frontend\templates\index.html" (
    cls
    echo.
    echo ============================================================
    echo ERROR: Frontend not found!
    echo ============================================================
    echo.
    echo Cannot find frontend\templates\index.html
    echo.
    echo Press any key to exit...
    pause >nul
    exit /b 1
)
echo [OK] Backend and frontend found!
echo.

REM Start server
echo [5/5] Starting server...
echo.
echo ============================================================
echo    SERVER STARTING
echo ============================================================
echo.
echo The web interface will open in your browser at:
echo    http://localhost:%PORT%
echo.
echo The server window will stay open while running.
echo Press Ctrl+C to stop the server when done.
echo.
echo ============================================================
echo.

REM Open browser
timeout /t 2 /nobreak >nul
start http://localhost:%PORT%

REM Run Flask
cd backend
set "PORT=%PORT%"
%PYTHON% app.py

REM When server stops
echo.
echo.
echo ============================================================
echo Server has stopped.
echo ============================================================
echo.
pause

