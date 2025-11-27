import { useState, useEffect, useRef } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { Search, Film, Loader2, TrendingUp, AlertCircle } from 'lucide-react'
import api from '../services/api'
import './Recommender.css'

const Recommender = ({ selectedMovie }) => {
    const [inputValue, setInputValue] = useState('')
    const [recommendations, setRecommendations] = useState([])
    const [loading, setLoading] = useState(false)
    const [error, setError] = useState(null)
    const [popularMovies, setPopularMovies] = useState([])
    const [searchSuggestions, setSearchSuggestions] = useState([])
    const [showDropdown, setShowDropdown] = useState(false)
    const [searchLoading, setSearchLoading] = useState(false)
    const dropdownRef = useRef(null)
    const searchBoxRef = useRef(null)

    useEffect(() => {
        loadPopularMovies()

        // Close dropdown when clicking outside
        const handleClickOutside = (event) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target) &&
                searchBoxRef.current && !searchBoxRef.current.contains(event.target)) {
                setShowDropdown(false)
            }
        }

        document.addEventListener('mousedown', handleClickOutside)
        return () => document.removeEventListener('mousedown', handleClickOutside)
    }, [])

    useEffect(() => {
        if (selectedMovie) {
            setInputValue(selectedMovie)
            handleGetRecommendations(selectedMovie)
        }
    }, [selectedMovie])

    // Search for movies as user types
    useEffect(() => {
        const searchMovies = async () => {
            if (inputValue.length >= 2) {
                setSearchLoading(true)
                try {
                    const results = await api.searchMovies(inputValue, 10)
                    setSearchSuggestions(results)
                    setShowDropdown(true)
                } catch (err) {
                    console.error('Error searching movies:', err)
                    setSearchSuggestions([])
                } finally {
                    setSearchLoading(false)
                }
            } else {
                setSearchSuggestions([])
                setShowDropdown(false)
            }
        }

        const debounceTimer = setTimeout(searchMovies, 300)
        return () => clearTimeout(debounceTimer)
    }, [inputValue])

    const loadPopularMovies = async () => {
        try {
            const data = await api.getTrending(5)
            setPopularMovies(data.map(m => m.title))
        } catch (err) {
            console.error('Error loading popular movies:', err)
            setPopularMovies(["Toy Story (1995)", "Jumanji (1995)", "Heat (1995)"])
        }
    }

    const handleGetRecommendations = async (movie = inputValue) => {
        if (!movie) return

        setLoading(true)
        setRecommendations([])
        setError(null)
        setShowDropdown(false)

        try {
            const data = await api.getRecommendations(movie, 10, 'cosine')
            setRecommendations(data.recommendations)
            setInputValue(data.input_movie) // Use the exact movie title from API
        } catch (err) {
            console.error('Error getting recommendations:', err)
            setError(err.message || 'Failed to get recommendations')
        } finally {
            setLoading(false)
        }
    }

    const handleTagClick = (movie) => {
        setInputValue(movie)
        setShowDropdown(false)
        handleGetRecommendations(movie)
    }

    const handleDropdownItemClick = (movie) => {
        setInputValue(movie)
        setShowDropdown(false)
        handleGetRecommendations(movie)
    }

    const handleKeyPress = (e) => {
        if (e.key === 'Enter') {
            handleGetRecommendations()
        }
    }

    const handleInputChange = (e) => {
        setInputValue(e.target.value)
    }

    return (
        <section className="recommender-section" id="recommender">
            <div className="recommender-container">
                <motion.div
                    className="recommender-input"
                    initial={{ opacity: 0, x: -50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <h2>What did you enjoy lately?</h2>
                    <p>Type a movie title to get similar recommendations</p>

                    <div className="search-box" ref={searchBoxRef}>
                        <Search size={20} />
                        <input
                            type="text"
                            value={inputValue}
                            onChange={handleInputChange}
                            onKeyPress={handleKeyPress}
                            onFocus={() => inputValue.length >= 2 && setShowDropdown(true)}
                            placeholder="e.g., Toy Story, Jumanji..."
                        />
                        <button
                            className="btn-search"
                            onClick={() => handleGetRecommendations()}
                            disabled={loading}
                        >
                            {loading ? <Loader2 size={18} className="spinner" /> : 'Recommend'}
                        </button>

                        {/* Dropdown for search suggestions */}
                        <AnimatePresence>
                            {showDropdown && searchSuggestions.length > 0 && (
                                <motion.div
                                    ref={dropdownRef}
                                    className="search-dropdown"
                                    initial={{ opacity: 0, y: -10 }}
                                    animate={{ opacity: 1, y: 0 }}
                                    exit={{ opacity: 0, y: -10 }}
                                    transition={{ duration: 0.2 }}
                                >
                                    {searchSuggestions.map((movie, index) => (
                                        <div
                                            key={movie.id || index}
                                            className="dropdown-item"
                                            onClick={() => handleDropdownItemClick(movie.title)}
                                        >
                                            <Film size={18} style={{ color: '#667eea' }} />
                                            <div>
                                                <div className="dropdown-item-text">{movie.title}</div>
                                            </div>
                                        </div>
                                    ))}
                                </motion.div>
                            )}
                        </AnimatePresence>
                    </div>

                    <div className="tags">
                        {popularMovies.map((movie) => (
                            <span key={movie} onClick={() => handleTagClick(movie)}>
                                {movie}
                            </span>
                        ))}
                    </div>
                </motion.div>


                <motion.div
                    className="recommender-results"
                    initial={{ opacity: 0, x: 50 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ duration: 0.6 }}
                >
                    <AnimatePresence mode="wait">
                        {loading ? (
                            <motion.div
                                key="loading"
                                className="placeholder-state"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                <Loader2 size={48} className="spinner" />
                                <p>Analyzing viewing patterns...</p>
                            </motion.div>
                        ) : error ? (
                            <motion.div
                                key="error"
                                className="placeholder-state error"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                <AlertCircle size={48} />
                                <p>{error}</p>
                                <button className="retry-btn" onClick={() => handleGetRecommendations()}>
                                    Try Again
                                </button>
                            </motion.div>
                        ) : recommendations.length > 0 ? (
                            <motion.div
                                key="results"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                <h3>
                                    Because you watched <span className="highlight">{inputValue}</span>
                                </h3>
                                <div className="results-list">
                                    {recommendations.map((movie, index) => {
                                        // Dynamic gradient colors for each movie
                                        const gradients = [
                                            'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                                            'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
                                            'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                                            'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
                                            'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
                                            'linear-gradient(135deg, #30cfd0 0%, #330867 100%)',
                                            'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
                                            'linear-gradient(135deg, #ff9a56 0%, #ff6a88 100%)',
                                            'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)',
                                            'linear-gradient(135deg, #ff6e7f 0%, #bfe9ff 100%)'
                                        ]
                                        const gradient = gradients[index % gradients.length]

                                        return (
                                            <motion.div
                                                key={movie.id}
                                                className="result-item"
                                                initial={{ opacity: 0, y: 20 }}
                                                animate={{ opacity: 1, y: 0 }}
                                                transition={{ delay: index * 0.1 }}
                                            >
                                                <div
                                                    className="result-poster-placeholder"
                                                    style={{ background: gradient }}
                                                >
                                                    <Film size={28} className="poster-icon" />
                                                </div>
                                                <div className="result-info">
                                                    <h4>{movie.title}</h4>
                                                    <div className="result-meta">{movie.genres}</div>
                                                    <div className="result-footer">
                                                        <div className="match-score">
                                                            <TrendingUp size={14} />
                                                            {movie.match} Match
                                                        </div>
                                                        <div className="result-rank">#{index + 1}</div>
                                                    </div>
                                                </div>
                                            </motion.div>
                                        )
                                    })}
                                </div>
                            </motion.div>
                        ) : (
                            <motion.div
                                key="placeholder"
                                className="placeholder-state"
                                initial={{ opacity: 0 }}
                                animate={{ opacity: 1 }}
                                exit={{ opacity: 0 }}
                            >
                                <Film size={48} />
                                <p>Recommendations will appear here</p>
                            </motion.div>
                        )}
                    </AnimatePresence>
                </motion.div>
            </div>
        </section>
    )
}

export default Recommender
