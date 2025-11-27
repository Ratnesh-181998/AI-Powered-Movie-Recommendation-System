# Contributing to ZeeMovies

First off, thank you for considering contributing to ZeeMovies! It's people like you that make this project better for everyone.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Style Guidelines](#style-guidelines)
- [Community](#community)

## 📜 Code of Conduct

This project and everyone participating in it is governed by our commitment to providing a welcoming and inspiring community for all. Please be respectful and constructive in your interactions.

### Our Standards

- **Be Respectful**: Treat everyone with respect and kindness
- **Be Collaborative**: Work together and help each other
- **Be Professional**: Keep discussions focused and productive
- **Be Open**: Welcome newcomers and different perspectives

## 🤝 How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues to avoid duplicates.

**When submitting a bug report, include:**
- Clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Screenshots (if applicable)
- Environment details (OS, Python version, Node version)
- Relevant log files

**Example:**
```markdown
**Bug**: Recommendations not loading for certain movies

**Steps to Reproduce:**
1. Search for "The Matrix"
2. Click "Recommend"
3. Observe error message

**Expected**: Should show 10 recommendations
**Actual**: Shows error "Movie not found"

**Environment:**
- OS: Windows 11
- Python: 3.11
- Browser: Chrome 120
```

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues.

**Include:**
- Clear, descriptive title
- Detailed description of the proposed feature
- Why this enhancement would be useful
- Possible implementation approach
- Examples or mockups (if applicable)

### Your First Code Contribution

Unsure where to begin? Look for issues labeled:
- `good first issue` - Simple issues perfect for beginners
- `help wanted` - Issues where we need community help
- `documentation` - Documentation improvements

## 🛠️ Development Setup

### Prerequisites

- Python 3.8+
- Node.js 16+
- Git

### Setup Steps

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub
   ```

2. **Clone your fork**
   ```bash
   git clone https://github.com/YOUR-USERNAME/AI-Powered-Movie-Recommendation-System.git
   cd AI-Powered-Movie-Recommendation-System
   ```

3. **Add upstream remote**
   ```bash
   git remote add upstream https://github.com/Ratnesh-181998/AI-Powered-Movie-Recommendation-System.git
   ```

4. **Set up backend**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # source .venv/bin/activate  # Linux/Mac
   cd backend
   pip install -r requirements.txt
   ```

5. **Set up frontend**
   ```bash
   cd frontend
   npm install
   ```

6. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 🔄 Pull Request Process

### Before Submitting

1. **Update your fork**
   ```bash
   git fetch upstream
   git rebase upstream/main
   ```

2. **Test your changes**
   - Run the application and verify it works
   - Test all affected features
   - Check for console errors
   - Review logs for warnings

3. **Follow style guidelines** (see below)

4. **Update documentation**
   - Update README if needed
   - Add comments to complex code
   - Update API documentation if endpoints changed

### Submitting the PR

1. **Push to your fork**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create Pull Request**
   - Go to the original repository
   - Click "New Pull Request"
   - Select your fork and branch
   - Fill out the PR template

3. **PR Title Format**
   ```
   [Type] Brief description
   
   Examples:
   [Feature] Add user authentication
   [Fix] Resolve recommendation loading issue
   [Docs] Update API documentation
   [Refactor] Improve data service performance
   ```

4. **PR Description Should Include:**
   - What changes were made
   - Why these changes were necessary
   - How to test the changes
   - Screenshots (if UI changes)
   - Related issues (if any)

### After Submission

- Respond to review comments promptly
- Make requested changes in new commits
- Keep the PR focused on a single feature/fix
- Be patient and respectful

## 📝 Style Guidelines

### Python Code Style

Follow **PEP 8** guidelines:

```python
# Good
def get_movie_recommendations(movie_id, top_n=10):
    """
    Get movie recommendations based on similarity.
    
    Args:
        movie_id: ID of the movie
        top_n: Number of recommendations to return
        
    Returns:
        List of recommended movies
    """
    recommendations = recommender_service.get_cosine_recommendations(
        movie_id, 
        top_n
    )
    return recommendations

# Bad
def getMovieRecs(id,n):
    recs=recommender_service.get_cosine_recommendations(id,n)
    return recs
```

**Key Points:**
- Use 4 spaces for indentation
- Maximum line length: 100 characters
- Use descriptive variable names
- Add docstrings to functions
- Use type hints where appropriate

### JavaScript/React Code Style

Follow modern React best practices:

```javascript
// Good
const MovieCard = ({ movie, onHover }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  
  const handleMouseEnter = () => {
    setIsPlaying(true);
    onHover?.(movie.id);
  };
  
  return (
    <div className="movie-card" onMouseEnter={handleMouseEnter}>
      <h3>{movie.title}</h3>
      {isPlaying && <VideoPreview src={movie.trailer} />}
    </div>
  );
};

// Bad
const moviecard = (props) => {
  const [playing,setplaying] = useState(false)
  return <div className="movie-card"><h3>{props.movie.title}</h3></div>
}
```

**Key Points:**
- Use functional components with hooks
- Use camelCase for variables and functions
- Use PascalCase for components
- Add PropTypes or TypeScript types
- Keep components focused and small

### Commit Message Guidelines

Use conventional commits format:

```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance tasks

**Examples:**
```
feat(recommender): add Pearson correlation algorithm

Implemented Pearson correlation as an alternative to cosine similarity
for generating movie recommendations. Users can now choose between
methods via the API.

Closes #42
```

```
fix(api): resolve CORS issue for production deployment

Added proper CORS headers to allow frontend requests from
different origins in production environment.
```

### Documentation Style

- Use clear, concise language
- Include code examples
- Add screenshots for UI features
- Keep documentation up-to-date
- Use proper markdown formatting

## 🧪 Testing Guidelines

### Backend Testing

```python
# Example test
def test_get_recommendations():
    """Test recommendation endpoint returns valid results"""
    response = client.post('/api/recommend', json={
        'movie_title': 'Toy Story',
        'top_n': 5
    })
    
    assert response.status_code == 200
    data = response.get_json()
    assert len(data['recommendations']) == 5
    assert 'title' in data['recommendations'][0]
```

### Frontend Testing

```javascript
// Example test
test('MovieCard displays movie title', () => {
  const movie = { id: 1, title: 'Toy Story' };
  render(<MovieCard movie={movie} />);
  
  expect(screen.getByText('Toy Story')).toBeInTheDocument();
});
```

## 🌟 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

## 💬 Community

### Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Pull Requests**: For code review and collaboration

### Contact

- **Project Maintainer**: Ratnesh Kumar
- **GitHub**: [@Ratnesh-181998](https://github.com/Ratnesh-181998)
- **LinkedIn**: [ratneshkumar1998](https://www.linkedin.com/in/ratneshkumar1998/)

## 📚 Additional Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://reactjs.org/)
- [Python PEP 8](https://pep8.org/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

Thank you for contributing to ZeeMovies! 🎬✨

**Remember**: Every contribution, no matter how small, is valuable and appreciated!
