import { useState } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import { PlayCircle, ChevronDown } from 'lucide-react'
import './Navbar.css'

const Navbar = () => {
    const [selectedCountry, setSelectedCountry] = useState('US')
    const [showCountryDropdown, setShowCountryDropdown] = useState(false)

    const countries = [
        { code: 'US', name: 'United States', flag: '🇺🇸' },
        { code: 'IN', name: 'India', flag: '🇮🇳' },
        { code: 'GB', name: 'United Kingdom', flag: '🇬🇧' },
        { code: 'CA', name: 'Canada', flag: '🇨🇦' },
        { code: 'AU', name: 'Australia', flag: '🇦🇺' },
        { code: 'FR', name: 'France', flag: '🇫🇷' },
        { code: 'DE', name: 'Germany', flag: '🇩🇪' },
        { code: 'JP', name: 'Japan', flag: '🇯🇵' },
    ]

    const handleCountrySelect = (countryCode) => {
        setSelectedCountry(countryCode)
        setShowCountryDropdown(false)
    }

    const currentCountry = countries.find(c => c.code === selectedCountry)

    return (
        <motion.nav
            className="navbar"
            initial={{ y: -100 }}
            animate={{ y: 0 }}
            transition={{ duration: 0.5 }}
        >
            <div className="logo">
                <PlayCircle size={32} />
                <span>ZEE<span className="highlight">MOVIES</span></span>
            </div>
            <ul className="nav-links">
                <li><a href="#" className="active">Home</a></li>
                <li><a href="#trending">Movies</a></li>
                <li><a href="#recommender">AI Picks</a></li>
                <li><a href="#about">About</a></li>
            </ul>
            <div className="navbar-right">
                <div className="country-selector">
                    <button
                        className="country-button"
                        onClick={() => setShowCountryDropdown(!showCountryDropdown)}
                    >
                        <span className="country-flag">{currentCountry.flag}</span>
                        <span className="country-code">{currentCountry.code}</span>
                        <ChevronDown size={16} className={showCountryDropdown ? 'rotate' : ''} />
                    </button>

                    <AnimatePresence>
                        {showCountryDropdown && (
                            <motion.div
                                className="country-dropdown"
                                initial={{ opacity: 0, y: -10 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -10 }}
                                transition={{ duration: 0.2 }}
                            >
                                {countries.map((country) => (
                                    <div
                                        key={country.code}
                                        className={`country-option ${selectedCountry === country.code ? 'selected' : ''}`}
                                        onClick={() => handleCountrySelect(country.code)}
                                    >
                                        <span className="country-flag">{country.flag}</span>
                                        <span className="country-name">{country.name}</span>
                                        {selectedCountry === country.code && (
                                            <span className="check-mark">✓</span>
                                        )}
                                    </div>
                                ))}
                            </motion.div>
                        )}
                    </AnimatePresence>
                </div>
                <div className="user-profile">
                    <img src="https://ui-avatars.com/api/?name=User&background=8e44ad&color=fff" alt="User" />
                </div>
            </div>
        </motion.nav>
    )
}

export default Navbar
