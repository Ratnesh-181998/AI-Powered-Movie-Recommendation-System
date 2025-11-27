import './Footer.css'

const Footer = () => {
    return (
        <footer className="footer">
            <div className="footer-content">
                <div className="footer-logo">
                    ZEE<span className="highlight">MOVIES</span>
                </div>
                <p>&copy; 2025 Zee Movie Recommender System. All rights reserved.</p>
                <p className="footer-tech">Powered by AI • Built with React & Python</p>
            </div>
        </footer>
    )
}

export default Footer
