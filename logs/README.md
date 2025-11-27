# ZeeMovies Application Logs

This directory contains all application logs generated during runtime.

## Log Files

### Startup Logs
- **Format**: `startup_YYYYMMDD_HHMMSS.log`
- **Contains**: Application startup sequence, initialization messages

### Backend Logs
- **Format**: `backend_YYYYMMDD_HHMMSS.log`
- **Contains**: API server logs, request/response data, errors
- **Location**: Also available in `backend/logs/` with rotating handlers

### Frontend Logs
- **Format**: `frontend_YYYYMMDD_HHMMSS.log`
- **Contains**: Vite dev server logs, build messages, hot reload events

### Detailed Backend Logs (in backend/logs/)
- **api.log**: General API operations and info messages
- **error.log**: Error messages and stack traces
- **access.log**: HTTP request access logs with response times

## Log Rotation

Backend logs use rotating file handlers:
- Maximum file size: 10MB
- Backup count: 5 files
- Older logs are automatically archived

## Viewing Logs

### Real-time monitoring (Windows):
```powershell
Get-Content logs\backend_*.log -Wait -Tail 50
```

### Real-time monitoring (Linux/Mac):
```bash
tail -f logs/backend_*.log
```

### Search for errors:
```bash
grep -i error logs/*.log
```

## Cleanup

Old log files can be safely deleted. The application will create new ones on next startup.

To clean logs older than 7 days:
```bash
# Linux/Mac
find logs/ -name "*.log" -mtime +7 -delete

# Windows PowerShell
Get-ChildItem logs\*.log | Where-Object {$_.LastWriteTime -lt (Get-Date).AddDays(-7)} | Remove-Item
```
