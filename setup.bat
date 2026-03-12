@echo off
echo ========================================
echo SmartClinic OS - Setup Script
echo ========================================
echo.

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Creating .env file...
if not exist .env (
    copy .env.example .env
    echo .env file created. Please update with your Twilio credentials if needed.
) else (
    echo .env file already exists.
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo 1. Run: venv\Scripts\activate
echo 2. Run: python app.py
echo 3. Open browser to: http://localhost:5000
echo.
echo Default credentials:
echo Receptionist: receptionist@clinic.com / receptionist123
echo Doctor: doctor@clinic.com / doctor123
echo.
pause
