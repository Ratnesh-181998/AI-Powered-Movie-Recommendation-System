from flask import Blueprint, request, jsonify
from app.utils.logger import api_logger, log_error
from app.utils.decorators import log_api_call
from app.services.data_service import data_service
from app.services.recommender import recommender_service
import traceback

api_bp = Blueprint('api', __name__)

@api_bp.route('/health', methods=['GET'])
@log_api_call
def health_check():
    """Health check endpoint"""
    api_logger.info("Health check requested")
    stats = data_service.get_stats()
    return jsonify({
        'status': 'healthy',
        'movies': stats['totalMovies'],
        'ratings': stats['totalRatings'],
        'users': stats['totalUsers']
    })

@api_bp.route('/movies', methods=['GET'])
@log_api_call
def get_movies():
    """Get all movies or search by title"""
    search = request.args.get('search', '').lower()
    limit = int(request.args.get('limit', 50))
    
    api_logger.info(f"Movies requested - search: '{search}', limit: {limit}")
    
    result = data_service.get_movies(search, limit)
    
    movies_list = []
    for _, row in result.iterrows():
        movies_list.append({
            'id': int(row['movie_id']),
            'title': row['title'],
            'genres': row['genres'],
            'avgRating': float(row['avg_rating']),
            'numRatings': int(row['num_ratings'])
        })
    
    api_logger.info(f"Returning {len(movies_list)} movies")
    return jsonify(movies_list)

@api_bp.route('/trending', methods=['GET'])
@log_api_call
def get_trending():
    """Get trending movies (most rated)"""
    limit = int(request.args.get('limit', 10))
    
    api_logger.info(f"Trending movies requested - limit: {limit}")
    
    result = data_service.get_trending(limit)
    
    trending_list = []
    for _, row in result.iterrows():
        trending_list.append({
            'id': int(row['movie_id']),
            'title': row['title'],
            'genres': row['genres'],
            'avgRating': float(row['avg_rating']),
            'numRatings': int(row['num_ratings'])
        })
    
    api_logger.info(f"Returning {len(trending_list)} trending movies")
    return jsonify(trending_list)

@api_bp.route('/recommend', methods=['POST'])
@log_api_call
def get_recommendations():
    """Get movie recommendations based on a movie title"""
    data = request.json
    movie_title = data.get('movie_title', '')
    top_n = data.get('top_n', 10)
    method = data.get('method', 'cosine')  # cosine or pearson
    
    api_logger.info(f"Recommendations requested - movie: '{movie_title}', method: {method}, top_n: {top_n}")
    
    if not movie_title:
        api_logger.warning("Recommendation request missing movie_title")
        return jsonify({'error': 'movie_title is required'}), 400
    
    # Find movie ID
    movie_match = data_service.find_movie_by_title(movie_title)
    
    if movie_match.empty:
        api_logger.warning(f"Movie not found: '{movie_title}'")
        return jsonify({'error': 'Movie not found'}), 404
    
    movie_id = movie_match.iloc[0]['movie_id']
    matched_title = movie_match.iloc[0]['title']
    
    api_logger.info(f"Found movie: '{matched_title}' (ID: {movie_id})")
    
    try:
        if method == 'cosine':
            recommendations = recommender_service.get_cosine_recommendations(movie_id, top_n)
        else:
            recommendations = recommender_service.get_pearson_recommendations(movie_id, top_n)
        
        api_logger.info(f"Generated {len(recommendations)} recommendations for '{matched_title}'")
        
        return jsonify({
            'input_movie': matched_title,
            'method': method,
            'recommendations': recommendations
        })
    except Exception as e:
        log_error(type(e).__name__, str(e), traceback.format_exc())
        return jsonify({'error': str(e)}), 500

@api_bp.route('/stats', methods=['GET'])
@log_api_call
def get_stats():
    """Get overall statistics"""
    api_logger.info("Statistics requested")
    
    stats = data_service.get_stats()
    
    api_logger.info(f"Returning stats: {stats['totalMovies']} movies, {stats['totalRatings']} ratings")
    return jsonify(stats)
