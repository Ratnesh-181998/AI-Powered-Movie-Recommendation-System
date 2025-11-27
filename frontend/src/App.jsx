import { useState } from 'react'
import { motion } from 'framer-motion'
import Navbar from './components/Navbar'
import Hero from './components/Hero'
import TrendingMovies from './components/TrendingMovies'
import Recommender from './components/Recommender'
import About from './components/About'
import Footer from './components/Footer'
import './App.css'

function App() {
  const [selectedMovie, setSelectedMovie] = useState('')

  const scrollToRecommender = () => {
    document.getElementById('recommender')?.scrollIntoView({ behavior: 'smooth' })
  }

  return (
    <div className="app">
      <Navbar />
      <Hero onGetRecommendations={scrollToRecommender} />
      <main className="container">
        <TrendingMovies onMovieClick={setSelectedMovie} />
        <Recommender selectedMovie={selectedMovie} />
        <About />
      </main>
      <Footer />
    </div>
  )
}

export default App
