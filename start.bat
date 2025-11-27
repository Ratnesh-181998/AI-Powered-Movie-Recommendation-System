@echo off
REM ZeeMovies Application Startup Script
REM This script starts both backend and frontend servers with logging

echo ========================================
echo    ZeeMovies Application Launcher
echo ========================================
echo.

REM Set the project root directory
set PROJECT_ROOT=%~dp0
cd /d %PROJECT_ROOT%

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs

REM Get current timestamp for log files
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set TIMESTAMP=%datetime:~0,8%_%datetime:~8,6%

echo [%date% %time%] Starting ZeeMovies Application... > logs\startup_%TIMESTAMP%.log

echo Starting Backend Server...
echo [%date% %time%] Starting Backend Server >> logs\startup_%TIMESTAMP%.log
start "ZeeMovies Backend" cmd /k "cd backend && ..\.venv\Scripts\activate && python run.py >> ..\logs\backend_%TIMESTAMP%.log 2>&1"

REM Wait for backend to start
timeout /t 5 /nobreak > nul

echo Starting Frontend Server...
echo [%date% %time%] Starting Frontend Server >> logs\startup_%TIMESTAMP%.log
start "ZeeMovies Frontend" cmd /k "cd frontend && npm run dev >> ..\logs\frontend_%TIMESTAMP%.log 2>&1"

echo.
echo ========================================
echo   Application Started Successfully!
echo ========================================
echo.
echo Backend:  http://localhost:5000
echo Frontend: http://localhost:5173
echo.
echo Logs are being written to the 'logs' folder
echo Backend Log:  logs\backend_%TIMESTAMP%.log
echo Frontend Log: logs\frontend_%TIMESTAMP%.log
echo Startup Log:  logs\startup_%TIMESTAMP%.log
echo.
echo Press any key to open the application in your browser...
pause > nul

REM Open the application in default browser
start http://localhost:5173

echo.
echo Application is running!
echo Close the terminal windows to stop the servers.
echo.
pause
