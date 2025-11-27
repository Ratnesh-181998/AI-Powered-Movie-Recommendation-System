import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import traceback
from app.utils.logger import api_logger, error_logger

class DataService:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DataService, cls).__new__(cls)
            cls._instance.ratings_df = None
            cls._instance.movies_df = None
            cls._instance.users_df = None
            cls._instance.movie_user_pivot = None
            cls._instance.item_similarity_matrix = None
            cls._instance.initialized = False
        return cls._instance

    def load_data(self):
        """Load and prepare data"""
        if self.initialized:
            return

        api_logger.info("Loading data...")
        
        try:
            # Load datasets
            self.ratings_df = pd.read_csv(
                './data/ratings.dat',
                sep='::',
                engine='python',
                header=0,
                names=['user_id', 'movie_id', 'rating', 'timestamp'],
                encoding='ISO-8859-1'
            )
            api_logger.info(f"Loaded {len(self.ratings_df)} ratings")
            
            self.movies_df = pd.read_csv(
                './data/movies.dat',
                sep='::',
                engine='python',
                header=0,
                names=['movie_id', 'title', 'genres'],
                encoding='ISO-8859-1'
            )
            api_logger.info(f"Loaded {len(self.movies_df)} movies")
            
            self.users_df = pd.read_csv(
                './data/users.dat',
                sep='::',
                engine='python',
                header=0,
                names=['user_id', 'gender', 'age', 'occupation', 'zip_code'],
                encoding='ISO-8859-1'
            )
            api_logger.info(f"Loaded {len(self.users_df)} users")
            
            # Create pivot table for recommendations
            api_logger.info("Creating pivot table...")
            self.movie_user_pivot = self.ratings_df.pivot_table(
                index='movie_id',
                columns='user_id',
                values='rating'
            ).fillna(0)
            
            # Pre-calculate item similarity matrix
            api_logger.info("Calculating similarity matrix...")
            self.item_similarity_matrix = cosine_similarity(self.movie_user_pivot)
            
            self.initialized = True
            api_logger.info("Data loaded successfully!")
            
        except Exception as e:
            error_logger.error(f"Failed to load data: {str(e)}")
            error_logger.error(traceback.format_exc())
            raise

    def get_movies(self, search='', limit=50):
        if not self.initialized:
            self.load_data()
            
        if search:
            filtered = self.movies_df[self.movies_df['title'].str.lower().str.contains(search.lower())]
        else:
            filtered = self.movies_df
        
        # Get movie stats
        movie_stats = self.ratings_df.groupby('movie_id').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        movie_stats.columns = ['movie_id', 'avg_rating', 'num_ratings']
        
        # Merge and sort
        result = filtered.merge(movie_stats, on='movie_id', how='left')
        result = result.fillna({'avg_rating': 0, 'num_ratings': 0})
        result = result.sort_values('num_ratings', ascending=False).head(limit)
        
        return result

    def get_trending(self, limit=10):
        if not self.initialized:
            self.load_data()

        movie_stats = self.ratings_df.groupby('movie_id').agg({
            'rating': ['mean', 'count']
        }).reset_index()
        movie_stats.columns = ['movie_id', 'avg_rating', 'num_ratings']
        
        # Filter movies with at least 100 ratings
        popular = movie_stats[movie_stats['num_ratings'] >= 100]
        popular = popular.sort_values('num_ratings', ascending=False).head(limit)
        
        result = popular.merge(self.movies_df, on='movie_id')
        return result

    def get_stats(self):
        if not self.initialized:
            self.load_data()
            
        return {
            'totalMovies': int(len(self.movies_df)),
            'totalRatings': int(len(self.ratings_df)),
            'totalUsers': int(len(self.users_df)),
            'avgRating': float(self.ratings_df['rating'].mean()),
            'sparsity': float((self.movie_user_pivot == 0).sum().sum() / (self.movie_user_pivot.shape[0] * self.movie_user_pivot.shape[1]) * 100)
        }

    def find_movie_by_title(self, title):
        if not self.initialized:
            self.load_data()
            
        movie_match = self.movies_df[self.movies_df['title'].str.lower() == title.lower()]
        
        if movie_match.empty:
            # Try partial match
            movie_match = self.movies_df[self.movies_df['title'].str.lower().str.contains(title.lower())]
            
        return movie_match

    def get_movie_details(self, movie_id):
        return self.movies_df[self.movies_df['movie_id'] == movie_id].iloc[0]

    def get_movie_ratings(self, movie_id):
        return self.ratings_df[self.ratings_df['movie_id'] == movie_id]

# Global instance
data_service = DataService()
