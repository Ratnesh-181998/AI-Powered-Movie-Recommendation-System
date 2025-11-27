import { useState, useEffect, useRef } from 'react'
import { motion } from 'framer-motion'
import { Flame, ChevronLeft, ChevronRight, Star, Loader2 } from 'lucide-react'
import api from '../services/api'
import './TrendingMovies.css'

const TrendingMovies = ({ onMovieClick }) => {
    const [movies, setMovies] = useState([])
    const [loading, setLoading] = useState(true)
    const [error, setError] = useState(null)
    const [hoveredCard, setHoveredCard] = useState(null)
    const videoRefs = useRef({})

    useEffect(() => {
        loadTrendingMovies()
    }, [])

    const loadTrendingMovies = async () => {
        try {
            setLoading(true)
            const data = await api.getTrending(10)
            setMovies(data)
            setError(null)
        } catch (err) {
            console.error('Error loading trending movies:', err)
            setError('Failed to load trending movies')
        } finally {
            setLoading(false)
        }
    }

    // Sample trailer URLs - In production, these would come from your API
    const getTrailerUrl = (index) => {
        const trailers = [
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ElephantsDream.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerEscapes.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerFun.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerJoyrides.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerMeltdowns.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/Sintel.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/SubaruOutbackOnStreetAndDirt.mp4',
            'https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/TearsOfSteel.mp4',
        ]
        return trailers[index % trailers.length]
    }

    const handleMouseEnter = (index) => {
        setHoveredCard(index)
        const video = videoRefs.current[index]
        if (video) {
            video.currentTime = 0 // Reset to start
            video.play().catch(err => console.log('Video play failed:', err))
        }
    }

    const handleMouseLeave = (index) => {
        setHoveredCard(null)
        const video = videoRefs.current[index]
        if (video) {
            video.pause()
            video.currentTime = 0
        }
    }

    const containerVariants = {
        hidden: { opacity: 0 },
        visible: {
            opacity: 1,
            transition: {
                staggerChildren: 0.1
            }
        }
    }

    const itemVariants = {
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 }
    }

    const getGenreColor = (genres) => {
        if (genres.includes('Action')) return '#e74c3c'
        if (genres.includes('Comedy')) return '#f39c12'
        if (genres.includes('Drama')) return '#3498db'
        if (genres.includes('Horror')) return '#9b59b6'
        return '#95a5a6'
    }

    if (loading) {
        return (
            <section className="trending-section" id="trending">
                <div className="section-header">
                    <h2>
                        <Flame size={28} />
                        Trending Now
                    </h2>
                </div>
                <div className="loading-container">
                    <Loader2 size={48} className="spinner" />
                    <p>Loading trending movies...</p>
                </div>
            </section>
        )
    }

    if (error) {
        return (
            <section className="trending-section" id="trending">
                <div className="section-header">
                    <h2>
                        <Flame size={28} />
                        Trending Now
                    </h2>
                </div>
                <div className="error-container">
                    <p>{error}</p>
                    <button onClick={loadTrendingMovies} className="retry-btn">Retry</button>
                </div>
            </section>
        )
    }

    return (
        <section className="trending-section" id="trending">
            <div className="section-header">
                <h2>
                    <Flame size={28} />
                    Trending Now
                </h2>
                <div className="controls">
                    <button className="control-btn">
                        <ChevronLeft size={20} />
                    </button>
                    <button className="control-btn">
                        <ChevronRight size={20} />
                    </button>
                </div>
            </div>

            <motion.div
                className="movie-grid"
                variants={containerVariants}
                initial="hidden"
                animate="visible"
            >
                {movies.map((movie, index) => (
                    <motion.div
                        key={movie.id}
                        className="movie-card"
                        variants={itemVariants}
                        whileHover={{ y: -10, scale: 1.02 }}
                        onClick={() => onMovieClick(movie.title)}
                        onMouseEnter={() => handleMouseEnter(index)}
                        onMouseLeave={() => handleMouseLeave(index)}
                    >
                        <div className="movie-poster-container">
                            <div
                                className="movie-poster-placeholder"
                                style={{
                                    background: `linear-gradient(135deg, ${getGenreColor(movie.genres)} 0%, #1a1a1f 100%)`
                                }}
                            >
                                <div className="movie-rank">#{index + 1}</div>
                                <div className="movie-genre-badge">{movie.genres.split('|')[0]}</div>
                            </div>

                            {/* Video Preview */}
                            <video
                                ref={el => videoRefs.current[index] = el}
                                className={`movie-video-preview ${hoveredCard === index ? 'active' : ''}`}
                                src={getTrailerUrl(index)}
                                muted
                                loop
                                playsInline
                                preload="metadata"
                            />

                            <div className="movie-overlay">
                                <button className="play-btn">▶</button>
                            </div>
                        </div>
                        <div className="movie-info">
                            <div className="movie-title" title={movie.title}>{movie.title}</div>
                            <div className="movie-meta">
                                <span>{movie.numRatings} ratings</span>
                                <span className="rating">
                                    <Star size={14} fill="currentColor" />
                                    {movie.avgRating.toFixed(1)}
                                </span>
                            </div>
                            <div className="movie-genre">{movie.genres.split('|').slice(0, 2).join(', ')}</div>
                        </div>
                    </motion.div>
                ))}
            </motion.div>
        </section>
    )
}

export default TrendingMovies
