@echo off
echo ====================================
echo   Third Eye - Starting Frontend
echo ====================================
echo.

cd frontend

if not exist "node_modules\" (
    echo Installing dependencies...
    call npm install
    echo.
)

echo Starting Next.js development server...
echo.
echo Frontend will be available at: http://localhost:3000
echo.

npm run dev
