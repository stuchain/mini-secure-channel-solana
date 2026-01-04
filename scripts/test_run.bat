@echo off
REM Quick diagnostics for the demo launcher

echo ============================================================
echo DIAGNOSTIC TEST - Secure Channel Demo
echo ============================================================
echo.
echo This script will test if everything is set up correctly.
echo.
pause

REM Go to repo root
cd /d "%~dp0"
echo Current directory: %CD%
echo.

REM Python
echo Testing Python...
python --version
if errorlevel 1 (
    echo [FAIL] Python not found!
    echo.
    echo Try: python3 --version
    python3 --version
) else (
    echo [OK] Python found!
)
echo.

REM Files
echo Testing requirements.txt...
if exist "requirements.txt" (
    echo [OK] requirements.txt found!
) else (
    echo [FAIL] requirements.txt not found!
    echo Current directory: %CD%
)
echo.

REM Frontend files
echo Testing frontend directory...
if exist "frontend" (
    echo [OK] frontend directory found!
    if exist "frontend\app.py" (
        echo [OK] app.py found!
    ) else (
        echo [FAIL] app.py not found in frontend!
    )
) else (
    echo [FAIL] frontend directory not found!
)
echo.

REM Flask
echo Testing Flask installation...
python -c "import flask; print('Flask version:', flask.__version__)"
if errorlevel 1 (
    echo [FAIL] Flask not installed!
    echo.
    echo Would you like to install dependencies now? (Y/N)
    set /p install="> "
    if /i "%install%"=="Y" (
        echo Installing dependencies...
        python -m pip install -r requirements.txt
    )
) else (
    echo [OK] Flask is installed!
)
echo.

echo ============================================================
echo Diagnostic complete!
echo ============================================================
echo.
echo If all tests passed, try running run.bat again.
echo If tests failed, fix the issues shown above.
echo.
pause

