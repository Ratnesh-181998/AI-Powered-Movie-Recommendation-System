# 🎯 How to See Logs in Action - Quick Guide

## ✅ Logging System is Now Active!

The API has been updated with comprehensive logging. Here's how to see it working:

## 📊 Step-by-Step Guide

### Step 1: Stop Current Server
In your backend terminal, press:
```
Ctrl + C
```

### Step 2: Restart with Logging
```bash
cd c:\Users\rattu\Downloads\Zee\backend
.venv\Scripts\activate
python api.py
```

### Step 3: Watch the Logs Being Created

You'll see output like this:
```
2025-11-27 04:34:24 - api - INFO - ================================================================================
2025-11-27 04:34:24 - api - INFO - ZeeMovies API Server Starting - 2025-11-27 04:34:24
2025-11-27 04:34:24 - api - INFO - ================================================================================
2025-11-27 04:34:24 - api - INFO - Loading data...
2025-11-27 04:34:25 - api - INFO - Loaded 1000209 ratings
2025-11-27 04:34:25 - api - INFO - Loaded 3883 movies
2025-11-27 04:34:25 - api - INFO - Loaded 6040 users
2025-11-27 04:34:25 - api - INFO - Creating pivot table...
2025-11-27 04:34:26 - api - INFO - Calculating similarity matrix...
2025-11-27 04:34:30 - api - INFO - Data loaded successfully!

==================================================
🚀 Zee Movie Recommender API
==================================================
📍 Running on: http://localhost:5000
📊 Endpoints:
   GET  /api/health
   GET  /api/movies?search=<query>&limit=<n>
   GET  /api/trending?limit=<n>
   POST /api/recommend
   GET  /api/stats
==================================================
📝 Logs are being written to:
   - backend/logs/api.log
   - backend/logs/error.log
   - backend/logs/access.log
==================================================
```

### Step 4: Check Log Files

Open a new PowerShell window:
```powershell
cd c:\Users\rattu\Downloads\Zee\backend\logs

# List log files
dir

# View api.log
Get-Content api.log

# Monitor in real-time
Get-Content api.log -Wait -Tail 20
```

### Step 5: Generate Some Logs

Use your frontend (http://localhost:5173) or use curl:

```powershell
# Health check
curl http://localhost:5000/api/health

# Get trending movies
curl http://localhost:5000/api/trending?limit=5

# Get recommendations
curl -X POST http://localhost:5000/api/recommend `
  -H "Content-Type: application/json" `
  -d '{"movie_title": "Toy Story", "top_n": 5}'
```

### Step 6: Watch Logs Update

In your real-time monitoring window, you'll see:
```
2025-11-27 04:35:00 - access - INFO - GET /api/health - Status: 200 - Time: 0.002s
2025-11-27 04:35:00 - api - INFO - Health check requested
2025-11-27 04:35:05 - access - INFO - GET /api/trending - Status: 200 - Time: 0.045s
2025-11-27 04:35:05 - api - INFO - Trending movies requested - limit: 5
2025-11-27 04:35:05 - api - INFO - Returning 5 trending movies
2025-11-27 04:35:10 - access - INFO - POST /api/recommend - Status: 200 - Time: 0.123s
2025-11-27 04:35:10 - api - INFO - Recommendations requested - movie: 'Toy Story', method: cosine, top_n: 5
2025-11-27 04:35:10 - api - INFO - Found movie: 'Toy Story (1995)' (ID: 1)
2025-11-27 04:35:10 - api - INFO - Generated 5 recommendations for 'Toy Story (1995)'
```

## 📂 Log File Locations

```
c:\Users\rattu\Downloads\Zee\backend\logs\
├── api.log        ← All API operations (INFO level)
├── error.log      ← Errors only (ERROR level)
└── access.log     ← HTTP requests with response times
```

## 🔍 What Each Log Contains

### api.log
- Server startup/shutdown
- Data loading progress
- API endpoint calls
- Business logic operations
- General information

### error.log
- Error messages
- Stack traces
- Failed operations
- Exception details

### access.log
- HTTP method and endpoint
- Response status code
- Response time in seconds
- Timestamp for each request

## 📊 Example Log Entries

### api.log
```
2025-11-27 04:34:24 - api - INFO - Loading data...
2025-11-27 04:34:25 - api - INFO - Loaded 1000209 ratings
2025-11-27 04:35:10 - api - INFO - Recommendations requested - movie: 'Toy Story', method: cosine, top_n: 5
```

### access.log
```
2025-11-27 04:35:00 - access - INFO - GET /api/health - Status: 200 - Time: 0.002s
2025-11-27 04:35:05 - access - INFO - GET /api/trending - Status: 200 - Time: 0.045s
2025-11-27 04:35:10 - access - INFO - POST /api/recommend - Status: 200 - Time: 0.123s
```

### error.log (when errors occur)
```
2025-11-27 04:36:00 - error - ERROR - ValueError: Movie not found
2025-11-27 04:36:00 - error - ERROR - Traceback: ...
```

## 🎯 Quick Commands

### View logs
```powershell
# All logs
Get-Content backend\logs\*.log

# Latest 20 lines
Get-Content backend\logs\api.log -Tail 20

# Real-time monitoring
Get-Content backend\logs\access.log -Wait -Tail 50

# Search for errors
Select-String -Path "backend\logs\*.log" -Pattern "error" -CaseSensitive:$false
```

### Clear old logs
```powershell
Remove-Item backend\logs\*.log
```

## ✨ Features

- ✅ **Automatic Rotation**: Files rotate at 10MB (keeps 5 backups)
- ✅ **Dual Output**: Logs go to both file and console
- ✅ **Performance Tracking**: Every request shows response time
- ✅ **Error Tracking**: Full stack traces for debugging
- ✅ **Structured Format**: Timestamp - Logger - Level - Message

## 🚀 Ready to Test!

Just restart your backend server and the logs will start flowing! 📊✨
