import numpy as np
from scipy.stats import pearsonr
from app.utils.logger import api_logger
from app.services.data_service import data_service

class RecommenderService:
    def get_cosine_recommendations(self, movie_id, top_n=10):
        """Get recommendations using cosine similarity"""
        if not data_service.initialized:
            data_service.load_data()
            
        try:
            movie_idx = data_service.movie_user_pivot.index.get_loc(movie_id)
        except KeyError:
            api_logger.warning(f"Movie ID {movie_id} not found in pivot table")
            return []
        
        # Get similarity scores
        similarity_scores = list(enumerate(data_service.item_similarity_matrix[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N (excluding the movie itself)
        top_similar = similarity_scores[1:top_n+1]
        
        recommendations = []
        for idx, score in top_similar:
            rec_movie_id = data_service.movie_user_pivot.index[idx]
            movie_info = data_service.get_movie_details(rec_movie_id)
            movie_ratings = data_service.get_movie_ratings(rec_movie_id)
            
            recommendations.append({
                'id': int(rec_movie_id),
                'title': movie_info['title'],
                'genres': movie_info['genres'],
                'similarity': float(score),
                'match': f"{int(score * 100)}%",
                'avgRating': float(movie_ratings['rating'].mean()) if len(movie_ratings) > 0 else 0,
                'numRatings': int(len(movie_ratings))
            })
        
        return recommendations

    def get_pearson_recommendations(self, movie_id, top_n=10):
        """Get recommendations using Pearson correlation"""
        if not data_service.initialized:
            data_service.load_data()

        try:
            target_movie_ratings = data_service.movie_user_pivot.loc[movie_id].dropna()
        except KeyError:
            api_logger.warning(f"Movie ID {movie_id} not found in pivot table")
            return []
        
        correlations = []
        
        for other_movie_id in data_service.movie_user_pivot.index:
            if other_movie_id == movie_id:
                continue
            
            other_movie_ratings = data_service.movie_user_pivot.loc[other_movie_id].dropna()
            
            # Find common users
            common_users = target_movie_ratings.index.intersection(other_movie_ratings.index)
            
            if len(common_users) > 5:
                corr, _ = pearsonr(
                    target_movie_ratings[common_users],
                    other_movie_ratings[common_users]
                )
                
                if not np.isnan(corr):
                    correlations.append({
                        'movie_id': other_movie_id,
                        'correlation': corr,
                        'common_users': len(common_users)
                    })
        
        # Sort by correlation
        correlations = sorted(correlations, key=lambda x: x['correlation'], reverse=True)[:top_n]
        
        recommendations = []
        for item in correlations:
            rec_movie_id = item['movie_id']
            movie_info = data_service.get_movie_details(rec_movie_id)
            movie_ratings = data_service.get_movie_ratings(rec_movie_id)
            
            recommendations.append({
                'id': int(rec_movie_id),
                'title': movie_info['title'],
                'genres': movie_info['genres'],
                'similarity': float(item['correlation']),
                'match': f"{int(item['correlation'] * 100)}%",
                'avgRating': float(movie_ratings['rating'].mean()) if len(movie_ratings) > 0 else 0,
                'numRatings': int(len(movie_ratings))
            })
        
        return recommendations

recommender_service = RecommenderService()
