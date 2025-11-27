#!/bin/bash
# ZeeMovies Application Startup Script (Linux/Mac)
# This script starts both backend and frontend servers with logging

echo "========================================"
echo "   ZeeMovies Application Launcher"
echo "========================================"
echo ""

# Set the project root directory
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$PROJECT_ROOT"

# Create logs directory if it doesn't exist
mkdir -p logs

# Get current timestamp for log files
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "[$(date)] Starting ZeeMovies Application..." > logs/startup_$TIMESTAMP.log

echo "Starting Backend Server..."
echo "[$(date)] Starting Backend Server" >> logs/startup_$TIMESTAMP.log
cd backend
source ../.venv/bin/activate
python run.py >> ../logs/backend_$TIMESTAMP.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 5

echo "Starting Frontend Server..."
echo "[$(date)] Starting Frontend Server" >> logs/startup_$TIMESTAMP.log
cd frontend
npm run dev >> ../logs/frontend_$TIMESTAMP.log 2>&1 &
FRONTEND_PID=$!
cd ..

echo ""
echo "========================================"
echo "  Application Started Successfully!"
echo "========================================"
echo ""
echo "Backend:  http://localhost:5000"
echo "Frontend: http://localhost:5173"
echo ""
echo "Logs are being written to the 'logs' folder"
echo "Backend Log:  logs/backend_$TIMESTAMP.log"
echo "Frontend Log: logs/frontend_$TIMESTAMP.log"
echo "Startup Log:  logs/startup_$TIMESTAMP.log"
echo ""
echo "Backend PID:  $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo ""
echo "Press Ctrl+C to stop all servers..."

# Save PIDs for cleanup
echo $BACKEND_PID > logs/backend.pid
echo $FRONTEND_PID > logs/frontend.pid

# Wait for interrupt
trap "echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; rm logs/*.pid 2>/dev/null; exit" INT TERM

# Keep script running
wait
