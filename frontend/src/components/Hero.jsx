import { motion } from 'framer-motion'
import { Sparkles, Info } from 'lucide-react'
import './Hero.css'

const Hero = ({ onGetRecommendations }) => {
    const scrollToAbout = () => {
        document.getElementById('about')?.scrollIntoView({ behavior: 'smooth' })
    }

    return (
        <div className="hero">
            <div className="hero-overlay"></div>
            <motion.div
                className="hero-content"
                initial={{ opacity: 0, x: -50 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.8, delay: 0.2 }}
            >
                <motion.span
                    className="badge"
                    initial={{ scale: 0 }}
                    animate={{ scale: 1 }}
                    transition={{ duration: 0.5, delay: 0.5 }}
                >
                    AI POWERED
                </motion.span>
                <h1>
                    Discover Your Next<br />
                    <span className="gradient-text">Favorite Movie</span>
                </h1>
                <p>
                    Our advanced recommendation engine analyzes your taste to curate the perfect watchlist just for you.
                </p>
                <div className="cta-buttons">
                    <motion.button
                        className="btn btn-primary"
                        onClick={onGetRecommendations}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <Sparkles size={20} />
                        Get Recommendations
                    </motion.button>
                    <motion.button
                        className="btn btn-secondary"
                        onClick={scrollToAbout}
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                    >
                        <Info size={20} />
                        Learn More
                    </motion.button>
                </div>
            </motion.div>
        </div>
    )
}

export default Hero
