@echo off
echo ========================================
echo   Helmet Detection - Starting Servers
echo ========================================
echo.

echo [1/2] Starting Backend Server...
start cmd /k "cd backend && python app.py"
timeout /t 3 /nobreak > nul

echo [2/2] Starting Frontend Server...
start cmd /k "cd frontend && npm run dev"

echo.
echo ========================================
echo   Servers are starting!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:3000
echo.
echo Opening browser in 5 seconds...
timeout /t 5 /nobreak > nul
start http://localhost:3000

echo.
echo Press any key to close this window...
pause > nul
