@echo off
echo ====================================
echo   Third Eye - Backend Setup
echo ====================================
echo.

echo Creating virtual environment...
python -m venv venv

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Installing dependencies...
pip install -r requirements.txt

echo.
echo ====================================
echo   Setup Complete!
echo ====================================
echo.
echo To start the server, run:
echo   python app.py
echo.
pause
