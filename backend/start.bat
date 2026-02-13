@echo off
echo ====================================
echo   Third Eye - Starting Backend
echo ====================================
echo.

if not exist "venv\" (
    echo Virtual environment not found!
    echo Please run setup.bat first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo.
echo Starting Flask server...
python app.py
