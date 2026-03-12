@echo off
echo ========================================
echo SmartClinic OS - Installation Test
echo ========================================
echo.

echo Checking Python installation...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo ✓ Python found
echo.

echo Checking virtual environment...
if exist venv\ (
    echo ✓ Virtual environment exists
) else (
    echo ✗ Virtual environment not found
    echo Run setup.bat first
    pause
    exit /b 1
)
echo.

echo Activating virtual environment...
call venv\Scripts\activate
echo.

echo Checking installed packages...
pip list | findstr Flask
if %errorlevel% neq 0 (
    echo ✗ Flask not installed
    echo Run setup.bat first
    pause
    exit /b 1
)
echo ✓ Flask installed
echo.

echo Checking project files...
if exist app.py (echo ✓ app.py) else (echo ✗ app.py missing)
if exist config.py (echo ✓ config.py) else (echo ✗ config.py missing)
if exist database.py (echo ✓ database.py) else (echo ✗ database.py missing)
if exist requirements.txt (echo ✓ requirements.txt) else (echo ✗ requirements.txt missing)
echo.

echo Checking directories...
if exist models\ (echo ✓ models/) else (echo ✗ models/ missing)
if exist routes\ (echo ✓ routes/) else (echo ✗ routes/ missing)
if exist services\ (echo ✓ services/) else (echo ✗ services/ missing)
if exist templates\ (echo ✓ templates/) else (echo ✗ templates/ missing)
if exist static\ (echo ✓ static/) else (echo ✗ static/ missing)
echo.

echo ========================================
echo Installation Test Complete!
echo ========================================
echo.
echo If all checks passed, you can run:
echo   run.bat
echo.
echo Then open browser to:
echo   http://localhost:5000
echo.
pause
