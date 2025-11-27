// API Configuration
const API_BASE_URL = 'http://localhost:5000/api'

// API Service
export const api = {
    // Health check
    async healthCheck() {
        const response = await fetch(`${API_BASE_URL}/health`)
        return response.json()
    },

    // Get all movies or search
    async getMovies(search = '', limit = 50) {
        const params = new URLSearchParams()
        if (search) params.append('search', search)
        params.append('limit', limit.toString())

        const response = await fetch(`${API_BASE_URL}/movies?${params}`)
        return response.json()
    },

    // Get trending movies
    async getTrending(limit = 10) {
        const response = await fetch(`${API_BASE_URL}/trending?limit=${limit}`)
        return response.json()
    },

    // Get recommendations
    async getRecommendations(movieTitle, topN = 10, method = 'cosine') {
        const response = await fetch(`${API_BASE_URL}/recommend`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                movie_title: movieTitle,
                top_n: topN,
                method: method
            })
        })

        if (!response.ok) {
            const error = await response.json()
            throw new Error(error.error || 'Failed to get recommendations')
        }

        return response.json()
    },

    // Get statistics
    async getStats() {
        const response = await fetch(`${API_BASE_URL}/stats`)
        return response.json()
    }
}

export default api
