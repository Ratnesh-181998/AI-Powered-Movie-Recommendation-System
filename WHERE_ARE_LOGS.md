# 📍 ZeeMovies Log Locations Guide

## Current Log Directory Structure

```
c:\Users\rattu\Downloads\Zee\logs\
├── .gitignore          ✅ (Prevents logs from being committed to git)
├── README.md           ✅ (Log documentation)
└── test_log.txt        ✅ (Test file - can be deleted)
```

## 📊 Where Log Files Will Be Created

### When you run `start.bat`, the following logs will be created:

```
c:\Users\rattu\Downloads\Zee\logs\
├── startup_20251127_042453.log      ⏳ Created on startup
├── backend_20251127_042453.log      ⏳ Backend server logs
└── frontend_20251127_042453.log     ⏳ Frontend server logs
```

**Note**: The timestamp `20251127_042453` will be replaced with the actual date/time when you start the app.

### Backend Detailed Logs (Rotating):

```
c:\Users\rattu\Downloads\Zee\backend\logs\
├── api.log              ⏳ General API logs (max 10MB, 5 backups)
├── api.log.1            ⏳ Backup 1 (when api.log reaches 10MB)
├── api.log.2            ⏳ Backup 2
├── error.log            ⏳ Error-only logs (max 10MB, 5 backups)
├── error.log.1          ⏳ Backup 1
└── access.log           ⏳ HTTP request logs (max 10MB, 5 backups)
```

## 🔍 How to View Logs

### Option 1: File Explorer
1. Open File Explorer
2. Navigate to: `c:\Users\rattu\Downloads\Zee\logs\`
3. Double-click any `.log` file to view in Notepad

### Option 2: PowerShell (Real-time monitoring)
```powershell
# Navigate to project directory
cd c:\Users\rattu\Downloads\Zee

# View latest backend log in real-time
Get-Content logs\backend_*.log -Wait -Tail 50

# View all logs
Get-ChildItem logs\*.log | ForEach-Object { Get-Content $_.FullName }

# Search for errors
Select-String -Path "logs\*.log" -Pattern "error" -CaseSensitive:$false
```

### Option 3: Command Prompt
```cmd
# Navigate to logs directory
cd c:\Users\rattu\Downloads\Zee\logs

# View a log file
type backend_*.log

# View last 20 lines
powershell "Get-Content backend_*.log -Tail 20"
```

### Option 4: VS Code
1. Open VS Code
2. File → Open Folder → Select `c:\Users\rattu\Downloads\Zee`
3. Expand `logs` folder in sidebar
4. Click on any log file to view

## 📝 Log File Contents

### startup_*.log
```
[2025-11-27 04:24:53] Starting ZeeMovies Application...
[2025-11-27 04:24:53] Starting Backend Server
[2025-11-27 04:24:58] Starting Frontend Server
```

### backend_*.log
```
Loading data...
Calculating similarity matrix...
Data loaded successfully!

========================================
🚀 Zee Movie Recommender API
========================================
📍 Running on: http://localhost:5000
📊 Endpoints:
   GET  /api/health
   GET  /api/movies?search=<query>&limit=<n>
   GET  /api/trending?limit=<n>
   POST /api/recommend
   GET  /api/stats
========================================
```

### frontend_*.log
```
VITE v5.0.0  ready in 1234 ms

➜  Local:   http://localhost:5173/
➜  Network: use --host to expose
➜  press h + enter to show help
```

### backend/logs/api.log
```
2025-11-27 04:25:00 - api - INFO - ================================================================================
2025-11-27 04:25:00 - api - INFO - ZeeMovies API Server Starting - 2025-11-27 04:25:00
2025-11-27 04:25:00 - api - INFO - ================================================================================
```

### backend/logs/access.log
```
2025-11-27 04:25:15 - access - INFO - GET /api/trending - Status: 200 - Time: 0.045s
2025-11-27 04:25:20 - access - INFO - POST /api/recommend - Status: 200 - Time: 0.123s
```

### backend/logs/error.log
```
2025-11-27 04:25:30 - error - ERROR - ValueError: Movie not found
2025-11-27 04:25:30 - error - ERROR - Traceback: ...
```

## 🚀 Quick Start to Generate Logs

1. **Stop current servers** (if running):
   - Press `Ctrl+C` in both terminal windows

2. **Run the startup script**:
   ```cmd
   start.bat
   ```

3. **Logs will be created immediately** in:
   - `c:\Users\rattu\Downloads\Zee\logs\`

4. **View logs**:
   ```powershell
   cd c:\Users\rattu\Downloads\Zee
   Get-ChildItem logs\*.log
   ```

## 📂 Current Actual Locations

**Main logs directory:**
```
c:\Users\rattu\Downloads\Zee\logs\
```

**Backend logs directory (will be created):**
```
c:\Users\rattu\Downloads\Zee\backend\logs\
```

## ✅ To See Logs NOW

Run this command in PowerShell:
```powershell
cd c:\Users\rattu\Downloads\Zee
.\start.bat
```

Then check:
```powershell
Get-ChildItem logs\*.log
```

You'll see all the log files created with timestamps! 📊✨
