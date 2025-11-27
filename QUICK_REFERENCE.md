# 🎬 ZeeMovies - Quick Reference Guide

## 🚀 Running the Application

### Option 1: Automated Startup (Recommended)
```bash
# Windows
.\start.bat

# Linux/Mac
./start.sh
```

### Option 2: Manual Startup
```bash
# Terminal 1 - Backend
cd backend
python run.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

---

## 🌐 Access URLs

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **Health Check:** http://localhost:5000/api/health

---

## 📡 API Endpoints

### GET /api/health
Health check endpoint
```bash
curl http://localhost:5000/api/health
```

### GET /api/movies?search=<query>&limit=<n>
Search for movies
```bash
curl "http://localhost:5000/api/movies?search=toy&limit=10"
```

### GET /api/trending?limit=<n>
Get trending movies
```bash
curl "http://localhost:5000/api/trending?limit=10"
```

### POST /api/recommend
Get movie recommendations
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie_title": "Toy Story", "top_n": 10, "method": "cosine"}'
```

### GET /api/stats
Get system statistics
```bash
curl http://localhost:5000/api/stats
```

---

## 📁 Project Structure

```
Zee/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App factory
│   │   ├── api/
│   │   │   └── routes.py        # API endpoints
│   │   ├── services/
│   │   │   ├── data_service.py  # Data management
│   │   │   └── recommender.py   # Algorithms
│   │   └── utils/
│   │       ├── logger.py        # Logging
│   │       └── decorators.py    # Decorators
│   ├── data/                    # MovieLens dataset
│   ├── logs/                    # Application logs
│   └── run.py                   # Entry point
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── Navbar.jsx       # Navigation
│   │   │   ├── Hero.jsx         # Landing
│   │   │   ├── TrendingMovies.jsx
│   │   │   ├── Recommender.jsx
│   │   │   ├── About.jsx
│   │   │   └── Footer.jsx
│   │   └── App.jsx              # Main app
│   └── package.json
│
├── logs/                        # Startup logs
├── start.bat                    # Windows startup
├── start.sh                     # Linux/Mac startup
└── README.md
```

---

## 📝 Log Files

### Backend Logs (backend/logs/)
- `api.log` - Application logs
- `access.log` - Request/response logs
- `error.log` - Error tracking

### Startup Logs (logs/)
- `startup_*.log` - Startup information
- `backend_*.log` - Backend output
- `frontend_*.log` - Frontend output

### View Logs
```bash
# Windows
type backend\logs\api.log
type logs\backend_*.log

# Linux/Mac
cat backend/logs/api.log
cat logs/backend_*.log
```

---

## 🔧 Common Tasks

### Stop Servers
```bash
# Press Ctrl+C in the terminal
# Or close the terminal windows
```

### Restart Backend Only
```bash
cd backend
python run.py
```

### Restart Frontend Only
```bash
cd frontend
npm run dev
```

### Clear Logs
```bash
# Windows
del /Q backend\logs\*.log
del /Q logs\*.log

# Linux/Mac
rm backend/logs/*.log
rm logs/*.log
```

### Check Server Status
```bash
# Windows
netstat -ano | findstr ":5000 :5173"

# Linux/Mac
lsof -i :5000
lsof -i :5173
```

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Windows - Kill process on port 5000
netstat -ano | findstr :5000
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Backend Not Starting
1. Check virtual environment is activated
2. Verify data files exist in `backend/data/`
3. Check logs in `backend/logs/error.log`

### Frontend Not Loading
1. Run `npm install` in frontend directory
2. Clear browser cache
3. Check console for errors

### Recommendations Not Working
1. Verify backend is running on port 5000
2. Check network tab in browser DevTools
3. Review `backend/logs/api.log`

---

## 📊 Performance

### Expected Response Times
- Trending movies: ~150ms
- Recommendations: ~300ms
- Movie search: ~120ms
- Stats: ~80ms

### Data Loaded
- 1,000,209 ratings
- 3,883 movies
- 6,040 users

---

## 🎨 Features

### Frontend
- ✅ Premium glassmorphism UI
- ✅ Country selector (8 countries)
- ✅ Video previews on hover
- ✅ Smooth scroll navigation
- ✅ Responsive design
- ✅ Animated components

### Backend
- ✅ Modular architecture
- ✅ Cosine similarity recommendations
- ✅ Pearson correlation recommendations
- ✅ Comprehensive logging
- ✅ Error handling
- ✅ Performance tracking

---

## 📚 Documentation

- `README.md` - Project overview
- `BACKEND_REFACTORING_COMPLETE.md` - Refactoring details
- `PROJECT_RUNNING_COMPLETE.md` - Current status
- `backend/REFACTORING_SUMMARY.md` - Technical summary
- `logs/README.md` - Logging guide

---

## 🎯 Quick Tests

### Test Recommendation
1. Open http://localhost:5173
2. Scroll to "Get Recommendations"
3. Type "Toy Story"
4. Click "Recommend"
5. View 10 similar movies

### Test API
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie_title": "Matrix", "top_n": 5}'
```

### Test Trending
1. Open http://localhost:5173
2. Scroll to "Trending Now"
3. Hover over movie cards
4. See video previews

---

## ✅ Status Check

**Backend:** ✅ Running on port 5000  
**Frontend:** ✅ Running on port 5173  
**Database:** ✅ Loaded (MovieLens dataset)  
**Logs:** ✅ Writing to backend/logs/  
**Features:** ✅ All working

---

**Need Help?** Check the documentation files or review the logs!
