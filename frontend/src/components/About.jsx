import { motion } from 'framer-motion'
import { Sparkles, Brain, TrendingUp, Film } from 'lucide-react'
import './About.css'

const About = () => {
    const features = [
        {
            icon: Brain,
            title: 'AI-Powered Recommendations',
            description: 'Our advanced machine learning algorithms analyze your preferences to suggest movies you\'ll love.'
        },
        {
            icon: TrendingUp,
            title: 'Trending Movies',
            description: 'Stay up-to-date with the most popular movies based on real-time viewing patterns.'
        },
        {
            icon: Film,
            title: 'Vast Movie Database',
            description: 'Access thousands of movies across all genres, from classics to the latest releases.'
        },
        {
            icon: Sparkles,
            title: 'Personalized Experience',
            description: 'Get recommendations tailored to your unique taste and viewing history.'
        }
    ]

    return (
        <section className="about-section" id="about">
            <div className="about-container">
                <motion.div
                    className="about-header"
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6 }}
                >
                    <h2>About ZeeMovies</h2>
                    <p className="about-subtitle">
                        Your intelligent movie companion powered by cutting-edge AI technology
                    </p>
                </motion.div>

                <motion.div
                    className="about-content"
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.2 }}
                >
                    <p className="about-description">
                        ZeeMovies is a revolutionary movie recommendation platform that combines the power of
                        artificial intelligence with an extensive movie database to help you discover your next
                        favorite film. Whether you're in the mood for action, romance, comedy, or thriller, our
                        smart recommendation engine understands your preferences and delivers personalized suggestions.
                    </p>
                </motion.div>

                <div className="features-grid">
                    {features.map((feature, index) => (
                        <motion.div
                            key={index}
                            className="feature-card"
                            initial={{ opacity: 0, y: 30 }}
                            whileInView={{ opacity: 1, y: 0 }}
                            viewport={{ once: true }}
                            transition={{ duration: 0.6, delay: index * 0.1 }}
                            whileHover={{ y: -10, scale: 1.02 }}
                        >
                            <div className="feature-icon">
                                <feature.icon size={32} />
                            </div>
                            <h3>{feature.title}</h3>
                            <p>{feature.description}</p>
                        </motion.div>
                    ))}
                </div>

                <motion.div
                    className="about-stats"
                    initial={{ opacity: 0, y: 30 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true }}
                    transition={{ duration: 0.6, delay: 0.4 }}
                >
                    <div className="stat-item">
                        <h3>10,000+</h3>
                        <p>Movies</p>
                    </div>
                    <div className="stat-item">
                        <h3>95%</h3>
                        <p>Accuracy</p>
                    </div>
                    <div className="stat-item">
                        <h3>1M+</h3>
                        <p>Recommendations</p>
                    </div>
                    <div className="stat-item">
                        <h3>24/7</h3>
                        <p>Available</p>
                    </div>
                </motion.div>
            </div>
        </section>
    )
}

export default About
