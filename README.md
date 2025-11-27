# 🎬 ZeeMovies - AI-Powered Movie Recommendation System

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![React](https://img.shields.io/badge/react-18.0+-61DAFB.svg)](https://reactjs.org/)
[![Flask](https://img.shields.io/badge/flask-3.0+-000000.svg)](https://flask.palletsprojects.com/)

An intelligent, production-ready movie recommendation platform powered by advanced machine learning algorithms, featuring a stunning React frontend and professionally architected Flask backend.

![ZeeMovies Banner](https://img.shields.io/badge/ZeeMovies-AI%20Powered-blueviolet?style=for-the-badge)

## 🌟 Features

### 🤖 AI-Powered Recommendations
- **Collaborative Filtering**: Advanced user-item matrix analysis
- **Cosine Similarity**: Fast, accurate recommendations
- **Pearson Correlation**: Alternative correlation-based recommendations
- **Pre-calculated Similarity Matrix**: Lightning-fast response times

### 🎥 Rich User Experience
- **Video Previews**: Hover-to-play movie trailers
- **Trending Movies**: Real-time trending based on 1M+ ratings
- **Smart Search**: Instant movie search with autocomplete
- **Country Selector**: Multi-region support (8 countries)
- **Glassmorphism UI**: Modern, premium design aesthetic
- **Smooth Animations**: Framer Motion powered transitions

### 🏗️ Professional Architecture
- **Modular Backend**: Clean separation of concerns
- **Service Layer Pattern**: Isolated business logic
- **Singleton Data Management**: Efficient resource usage
- **Flask Blueprints**: Scalable routing
- **Comprehensive Logging**: Rotating file handlers with performance tracking
- **Error Handling**: Robust exception management

## 📁 Project Structure

```
AI-Powered-Movie-Recommendation-System/
├── backend/                      # Flask API Server
│   ├── app/                      # Application package
│   │   ├── __init__.py          # App factory
│   │   ├── api/                 # API layer
│   │   │   ├── __init__.py
│   │   │   └── routes.py        # All API endpoints
│   │   ├── services/            # Business logic layer
│   │   │   ├── __init__.py
│   │   │   ├── data_service.py  # Data management (Singleton)
│   │   │   └── recommender.py   # Recommendation algorithms
│   │   └── utils/               # Utilities
│   │       ├── __init__.py
│   │       ├── logger.py        # Logging configuration
│   │       └── decorators.py    # Reusable decorators
│   ├── data/                    # MovieLens dataset
│   ├── logs/                    # Application logs
│   ├── run.py                   # Entry point
│   └── requirements.txt         # Python dependencies
│
├── frontend/                    # React Application
│   ├── src/
│   │   ├── components/         # React components
│   │   │   ├── Navbar.jsx      # Navigation with country selector
│   │   │   ├── Hero.jsx        # Landing section
│   │   │   ├── TrendingMovies.jsx  # Trending with video previews
│   │   │   ├── Recommender.jsx # Recommendation engine
│   │   │   ├── About.jsx       # About section
│   │   │   └── Footer.jsx      # Footer
│   │   ├── App.jsx             # Main application
│   │   └── main.jsx            # Entry point
│   └── package.json            # Node dependencies
│
├── logs/                       # Startup logs
├── start.bat                   # Windows startup script
├── start.sh                    # Linux/Mac startup script
├── LICENSE                     # MIT License
├── README.md                   # This file
├── QUICK_REFERENCE.md         # Quick start guide
└── BACKEND_REFACTORING_COMPLETE.md  # Architecture documentation
```

## 🚀 Quick Start

### Prerequisites

- **Python** 3.8 or higher
- **Node.js** 16 or higher
- **npm** or **yarn**
- **Git**

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Ratnesh-181998/AI-Powered-Movie-Recommendation-System.git
   cd AI-Powered-Movie-Recommendation-System
   ```

2. **Backend Setup**
   ```bash
   # Create virtual environment
   python -m venv .venv
   
   # Activate virtual environment
   # Windows:
   .venv\Scripts\activate
   # Linux/Mac:
   source .venv/bin/activate
   
   # Install dependencies
   cd backend
   pip install -r requirements.txt
   cd ..
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cd ..
   ```

### Running the Application

#### Option 1: Automated Startup (Recommended)

**Windows:**
```bash
.\start.bat
```

**Linux/Mac:**
```bash
chmod +x start.sh
./start.sh
```

The scripts will:
- ✅ Start both backend and frontend servers
- ✅ Create timestamped log files
- ✅ Open the application in your browser
- ✅ Display server URLs and log locations

#### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python run.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

### Accessing the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5000
- **API Health Check**: http://localhost:5000/api/health

## 📊 API Documentation

### Endpoints

#### `GET /api/health`
Health check endpoint

**Response:**
```json
{
  "status": "healthy",
  "movies": 3883,
  "ratings": 1000209,
  "users": 6040
}
```

#### `GET /api/movies`
Get all movies or search by title

**Query Parameters:**
- `search` (optional): Search query
- `limit` (optional): Number of results (default: 50)

**Example:**
```bash
curl "http://localhost:5000/api/movies?search=toy&limit=10"
```

#### `GET /api/trending`
Get trending movies based on ratings

**Query Parameters:**
- `limit` (optional): Number of results (default: 10)

**Example:**
```bash
curl "http://localhost:5000/api/trending?limit=5"
```

#### `POST /api/recommend`
Get movie recommendations

**Request Body:**
```json
{
  "movie_title": "Toy Story",
  "top_n": 10,
  "method": "cosine"
}
```

**Parameters:**
- `movie_title`: Movie name to base recommendations on
- `top_n`: Number of recommendations (default: 10)
- `method`: Algorithm to use - `cosine` or `pearson` (default: cosine)

**Example:**
```bash
curl -X POST http://localhost:5000/api/recommend \
  -H "Content-Type: application/json" \
  -d '{"movie_title": "Matrix", "top_n": 5, "method": "cosine"}'
```

#### `GET /api/stats`
Get overall system statistics

**Response:**
```json
{
  "totalMovies": 3883,
  "totalRatings": 1000209,
  "totalUsers": 6040,
  "avgRating": 3.58,
  "sparsity": 95.8
}
```

## 🛠️ Technology Stack

### Backend
| Technology | Purpose |
|------------|---------|
| **Flask** | Web framework |
| **Pandas** | Data manipulation |
| **NumPy** | Numerical computing |
| **Scikit-learn** | Machine learning (cosine similarity) |
| **SciPy** | Scientific computing (Pearson correlation) |
| **Flask-CORS** | Cross-origin resource sharing |

### Frontend
| Technology | Purpose |
|------------|---------|
| **React** | UI framework |
| **Vite** | Build tool & dev server |
| **Framer Motion** | Smooth animations |
| **Lucide React** | Beautiful icons |
| **Axios** | HTTP client |

### Data
- **MovieLens Dataset**: 1M+ ratings, 3,883 movies, 6,040 users

## 🎨 Features in Detail

### Recommendation Algorithms

#### Cosine Similarity (Default)
- Measures similarity between movie rating vectors
- Fast computation using pre-calculated matrix
- Ideal for sparse datasets
- Response time: ~300ms

#### Pearson Correlation
- Measures linear correlation between ratings
- Accounts for rating scale differences
- Better for users with similar rating patterns
- Response time: ~400ms

### UI/UX Features

- **Glassmorphism Design**: Modern frosted glass effect
- **Smooth Animations**: Framer Motion powered transitions
- **Video Previews**: Auto-play trailers on hover
- **Responsive Grid**: Adapts to all screen sizes
- **Dark Theme**: Eye-friendly color scheme
- **Country Selector**: 8 countries supported
  - 🇺🇸 United States
  - 🇮🇳 India
  - 🇬🇧 United Kingdom
  - 🇨🇦 Canada
  - 🇦🇺 Australia
  - 🇫🇷 France
  - 🇩🇪 Germany
  - 🇯🇵 Japan

## 📝 Logging System

### Log Files

All logs are stored with automatic rotation (10MB max per file, 5 backups):

**Backend Logs** (`backend/logs/`):
- `api.log` - Application logs (data loading, requests)
- `access.log` - HTTP access logs with response times
- `error.log` - Error tracking with stack traces

**Startup Logs** (`logs/`):
- `startup_*.log` - Application startup information
- `backend_*.log` - Backend server output
- `frontend_*.log` - Frontend dev server output

### Viewing Logs

**Real-time monitoring:**
```bash
# Windows PowerShell
Get-Content backend\logs\api.log -Wait -Tail 50

# Linux/Mac
tail -f backend/logs/api.log
```

**Search for errors:**
```bash
grep -i error backend/logs/*.log
```

## 📈 Performance Metrics

- **Dataset Size**: 1,000,209 ratings
- **Movies**: 3,883 unique titles
- **Users**: 6,040 active users
- **Recommendation Speed**: ~300ms average
- **Trending API**: ~150ms average
- **Search API**: ~120ms average
- **Similarity Matrix**: Pre-calculated for instant results

## 🔧 Development

### Backend Development

```bash
cd backend
python run.py
```

The backend uses:
- **App Factory Pattern** for clean initialization
- **Service Layer** for business logic separation
- **Singleton Pattern** for data management
- **Flask Blueprints** for modular routing

### Frontend Development

```bash
cd frontend
npm run dev
```

Hot reload enabled for instant updates.

### Building for Production

```bash
cd frontend
npm run build
```

Output will be in `frontend/dist/`

## 📦 Deployment

### Backend Deployment

1. Install production dependencies
2. Use a WSGI server (Gunicorn/Waitress)
3. Configure environment variables
4. Set up reverse proxy (Nginx/Apache)

**Example with Gunicorn:**
```bash
cd backend
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Frontend Deployment

1. Build the production bundle
2. Serve static files from `dist/`
3. Configure API endpoint

**Example with Nginx:**
```nginx
server {
    listen 80;
    server_name yourdomain.com;
    
    location / {
        root /path/to/frontend/dist;
        try_files $uri /index.html;
    }
    
    location /api {
        proxy_pass http://localhost:5000;
    }
}
```

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/AmazingFeature`)
3. **Commit** your changes (`git commit -m 'Add some AmazingFeature'`)
4. **Push** to the branch (`git push origin feature/AmazingFeature`)
5. **Open** a Pull Request

### Contribution Guidelines

- Follow existing code style
- Add tests for new features
- Update documentation
- Ensure all tests pass

## 🐛 Troubleshooting

### Port Already in Use

```bash
# Windows
netstat -ano | findstr :5000
taskkill /F /PID <PID>

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

### Backend Not Starting

1. Check virtual environment is activated
2. Verify data files exist in `backend/data/`
3. Review `backend/logs/error.log`

### Frontend Not Loading

1. Run `npm install` in frontend directory
2. Clear browser cache
3. Check console for errors

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

### Key Points:
- ✅ Free for personal and commercial use
- ✅ Attribution appreciated
- ✅ No warranty provided

## 👨‍💻 Author

**Ratnesh Kumar**

- 🐙 GitHub: [@Ratnesh-181998](https://github.com/Ratnesh-181998)
- 💼 LinkedIn: [ratneshkumar1998](https://www.linkedin.com/in/ratneshkumar1998/)
- 📧 Contact: Available via GitHub or LinkedIn

## 🙏 Acknowledgments

- **MovieLens** - For providing the comprehensive movie ratings dataset
- **GroupLens Research** - For their work in collaborative filtering
- **Open Source Community** - For amazing libraries and tools
- **React Team** - For the incredible UI framework
- **Flask Team** - For the lightweight and powerful web framework

## 📚 Additional Documentation

- [Quick Reference Guide](QUICK_REFERENCE.md) - Common commands and tasks
- [Backend Refactoring Report](BACKEND_REFACTORING_COMPLETE.md) - Architecture details
- [Project Status](PROJECT_RUNNING_COMPLETE.md) - Current implementation status

## 🎯 Roadmap

- [ ] User authentication and profiles
- [ ] Personalized recommendations based on watch history
- [ ] Integration with external movie APIs (TMDB)
- [ ] Real-time collaborative filtering
- [ ] Mobile app (React Native)
- [ ] Advanced analytics dashboard
- [ ] A/B testing framework
- [ ] Docker containerization
- [ ] Kubernetes deployment

## 📊 Project Stats

![GitHub stars](https://img.shields.io/github/stars/Ratnesh-181998/AI-Powered-Movie-Recommendation-System?style=social)
![GitHub forks](https://img.shields.io/github/forks/Ratnesh-181998/AI-Powered-Movie-Recommendation-System?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/Ratnesh-181998/AI-Powered-Movie-Recommendation-System?style=social)

---

<div align="center">

**Made with ❤️ and AI by Ratnesh Kumar**

⭐ Star this repo if you find it helpful!

[Report Bug](https://github.com/Ratnesh-181998/AI-Powered-Movie-Recommendation-System/issues) · [Request Feature](https://github.com/Ratnesh-181998/AI-Powered-Movie-Recommendation-System/issues)

</div>
