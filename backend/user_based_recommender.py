"""
USER-BASED COLLABORATIVE FILTERING
===================================
Recommender system based on user similarity using Pearson Correlation
"""

import pandas as pd
import numpy as np
from scipy.stats import pearsonr
import warnings
warnings.filterwarnings('ignore')


class UserBasedRecommender:
    """
    User-based Collaborative Filtering Recommender System
    """
    
    def __init__(self, ratings_df, movies_df):
        """
        Initialize User-based Recommender
        
        Parameters:
        -----------
        ratings_df : DataFrame with columns [user_id, movie_id, rating]
        movies_df : DataFrame with columns [movie_id, title, genres]
        """
        self.ratings = ratings_df
        self.movies = movies_df
        self.new_user_ratings = None
        
    def get_user_input(self, sample_movies=None, n_movies=10):
        """
        Get ratings from a new user
        
        Parameters:
        -----------
        sample_movies : list of movie titles to rate (optional)
        n_movies : number of movies to rate
        """
        print("\n" + "="*80)
        print("NEW USER RATING INPUT")
        print("="*80)
        
        if sample_movies is None:
            # Get popular movies for the user to rate
            popular_movies = (self.ratings.groupby('movie_id')
                            .size()
                            .sort_values(ascending=False)
                            .head(50)
                            .index.tolist())
            
            sample_movie_ids = np.random.choice(popular_movies, n_movies, replace=False)
            sample_movies = [
                self.movies[self.movies['movie_id'] == mid]['title'].values[0]
                for mid in sample_movie_ids
            ]
        
        print(f"\n👤 Please rate the following {len(sample_movies)} movies (1-5 stars, 0 if not watched):")
        print("-" * 80)
        
        # Simulate user ratings (in practice, this would be interactive input)
        # For demonstration, we'll use random ratings
        user_ratings = []
        
        for i, movie_title in enumerate(sample_movies, 1):
            # In real scenario: rating = int(input(f"{i}. {movie_title}: "))
            # For demo, simulate ratings
            rating = np.random.choice([0, 3, 4, 5], p=[0.3, 0.2, 0.3, 0.2])
            
            if rating > 0:
                movie_id = self.movies[self.movies['title'] == movie_title]['movie_id'].values[0]
                user_ratings.append({
                    'movie_id': movie_id,
                    'title': movie_title,
                    'rating': rating
                })
                print(f"   {i}. {movie_title}: {'⭐' * rating} ({rating}/5)")
            else:
                print(f"   {i}. {movie_title}: Not watched")
        
        self.new_user_ratings = pd.DataFrame(user_ratings)
        
        print(f"\n✅ Collected {len(self.new_user_ratings)} ratings from new user")
        
        return self.new_user_ratings
    
    def find_similar_users(self, top_n=100):
        """
        Find users who have watched the same movies as the new user
        
        Parameters:
        -----------
        top_n : Number of most similar users to consider
        """
        print("\n" + "="*80)
        print("FINDING SIMILAR USERS")
        print("="*80)
        
        if self.new_user_ratings is None or len(self.new_user_ratings) == 0:
            print("❌ No user ratings available!")
            return None
        
        # Get movies rated by new user
        new_user_movies = set(self.new_user_ratings['movie_id'].values)
        
        print(f"\n🔍 Finding users who watched the same movies...")
        print(f"   New user rated {len(new_user_movies)} movies")
        
        # Find users who have rated at least one of the same movies
        similar_users_data = self.ratings[
            self.ratings['movie_id'].isin(new_user_movies)
        ].copy()
        
        # Count common movies for each user
        common_movie_counts = (similar_users_data.groupby('user_id')
                              .size()
                              .sort_values(ascending=False))
        
        print(f"\n📊 Found {len(common_movie_counts)} users with common movies")
        print(f"   Max common movies: {common_movie_counts.max()}")
        print(f"   Avg common movies: {common_movie_counts.mean():.2f}")
        
        # Take top N users with most common movies
        top_users = common_movie_counts.head(top_n).index.tolist()
        
        print(f"\n✅ Selected top {len(top_users)} users for similarity calculation")
        
        return top_users, similar_users_data
    
    def calculate_user_similarity(self, top_users, similar_users_data):
        """
        Calculate Pearson Correlation similarity for each user
        
        Parameters:
        -----------
        top_users : List of user IDs to calculate similarity with
        similar_users_data : DataFrame with ratings from similar users
        """
        print("\n" + "="*80)
        print("CALCULATING USER SIMILARITY (Pearson Correlation)")
        print("="*80)
        
        similarities = []
        
        # Create a mapping of new user's ratings
        new_user_rating_map = dict(zip(
            self.new_user_ratings['movie_id'],
            self.new_user_ratings['rating']
        ))
        
        print(f"\n🔄 Calculating similarity for {len(top_users)} users...")
        
        for user_id in top_users:
            # Get ratings for this user
            user_ratings = similar_users_data[
                similar_users_data['user_id'] == user_id
            ]
            
            # Find common movies
            common_movies = set(user_ratings['movie_id'].values).intersection(
                set(new_user_rating_map.keys())
            )
            
            if len(common_movies) < 2:  # Need at least 2 common movies
                continue
            
            # Get ratings for common movies
            new_user_common_ratings = [new_user_rating_map[mid] for mid in common_movies]
            other_user_common_ratings = [
                user_ratings[user_ratings['movie_id'] == mid]['rating'].values[0]
                for mid in common_movies
            ]
            
            # Calculate Pearson correlation
            try:
                corr, _ = pearsonr(new_user_common_ratings, other_user_common_ratings)
                
                if not np.isnan(corr) and corr > 0:  # Only positive correlations
                    similarities.append({
                        'user_id': user_id,
                        'similarity': corr,
                        'common_movies': len(common_movies)
                    })
            except:
                continue
        
        similarities_df = pd.DataFrame(similarities)
        similarities_df = similarities_df.sort_values('similarity', ascending=False)
        
        print(f"\n✅ Calculated similarity for {len(similarities_df)} users")
        print(f"   Max similarity: {similarities_df['similarity'].max():.4f}")
        print(f"   Avg similarity: {similarities_df['similarity'].mean():.4f}")
        
        return similarities_df
    
    def get_recommendations(self, similarities_df, top_similar_users=10, top_n_movies=10):
        """
        Get movie recommendations based on similar users
        
        Parameters:
        -----------
        similarities_df : DataFrame with user similarities
        top_similar_users : Number of most similar users to use
        top_n_movies : Number of movies to recommend
        """
        print("\n" + "="*80)
        print(f"GENERATING RECOMMENDATIONS (Top {top_similar_users} Similar Users)")
        print("="*80)
        
        # Get top similar users
        top_similar = similarities_df.head(top_similar_users)
        
        print(f"\n👥 Using {len(top_similar)} most similar users:")
        for idx, row in top_similar.head(5).iterrows():
            print(f"   User {row['user_id']}: Similarity = {row['similarity']:.4f}, Common Movies = {row['common_movies']}")
        if len(top_similar) > 5:
            print(f"   ... and {len(top_similar) - 5} more users")
        
        # Get all movies rated by similar users
        similar_user_ids = top_similar['user_id'].tolist()
        similar_user_ratings = self.ratings[
            self.ratings['user_id'].isin(similar_user_ids)
        ].copy()
        
        # Exclude movies already rated by new user
        new_user_movies = set(self.new_user_ratings['movie_id'].values)
        candidate_movies = similar_user_ratings[
            ~similar_user_ratings['movie_id'].isin(new_user_movies)
        ].copy()
        
        # Merge with similarity scores
        candidate_movies = candidate_movies.merge(
            top_similar[['user_id', 'similarity']],
            on='user_id'
        )
        
        # Calculate weighted rating
        candidate_movies['weighted_rating'] = (
            candidate_movies['rating'] * candidate_movies['similarity']
        )
        
        # Group by movie and calculate average recommendation score
        movie_scores = candidate_movies.groupby('movie_id').agg({
            'weighted_rating': 'sum',
            'similarity': 'sum',
            'rating': 'count'
        }).reset_index()
        
        movie_scores.columns = ['movie_id', 'weighted_rating_sum', 'similarity_sum', 'num_ratings']
        
        # Calculate recommendation score
        movie_scores['recommendation_score'] = (
            movie_scores['weighted_rating_sum'] / movie_scores['similarity_sum']
        )
        
        # Sort by recommendation score
        movie_scores = movie_scores.sort_values('recommendation_score', ascending=False)
        
        # Get top N recommendations
        top_recommendations = movie_scores.head(top_n_movies)
        
        # Merge with movie titles
        top_recommendations = top_recommendations.merge(
            self.movies[['movie_id', 'title', 'genres']],
            on='movie_id'
        )
        
        print(f"\n🎬 Top {top_n_movies} Movie Recommendations:")
        print("=" * 80)
        
        for idx, row in top_recommendations.iterrows():
            print(f"\n{list(top_recommendations.index).index(idx) + 1}. {row['title']}")
            print(f"   Recommendation Score: {row['recommendation_score']:.2f}/5.0")
            print(f"   Based on {int(row['num_ratings'])} ratings from similar users")
            print(f"   Genres: {row['genres']}")
        
        return top_recommendations
    
    def run_user_based_recommendation(self, sample_movies=None, n_movies_to_rate=10,
                                     top_similar_users=10, top_n_recommendations=10):
        """
        Complete user-based recommendation pipeline
        
        Parameters:
        -----------
        sample_movies : List of movie titles for user to rate
        n_movies_to_rate : Number of movies to ask user to rate
        top_similar_users : Number of similar users to use
        top_n_recommendations : Number of recommendations to generate
        """
        print("\n" + "🎯"*40)
        print(" "*25 + "USER-BASED COLLABORATIVE FILTERING")
        print("🎯"*40)
        
        # Step 1: Get user ratings
        self.get_user_input(sample_movies, n_movies_to_rate)
        
        # Step 2: Find similar users
        top_users, similar_users_data = self.find_similar_users(top_n=100)
        
        # Step 3: Calculate user similarity
        similarities_df = self.calculate_user_similarity(top_users, similar_users_data)
        
        # Step 4: Get recommendations
        recommendations = self.get_recommendations(
            similarities_df,
            top_similar_users=top_similar_users,
            top_n_movies=top_n_recommendations
        )
        
        print("\n" + "="*80)
        print("✅ USER-BASED RECOMMENDATION COMPLETED!")
        print("="*80)
        
        return recommendations


def main_user_based(ratings_df, movies_df):
    """Main function for User-based Collaborative Filtering"""
    print("\n" + "👥"*40)
    print(" "*20 + "USER-BASED COLLABORATIVE FILTERING RECOMMENDER")
    print("👥"*40 + "\n")
    
    # Initialize recommender
    user_recommender = UserBasedRecommender(
        ratings_df=ratings_df,
        movies_df=movies_df
    )
    
    # Run recommendation pipeline
    recommendations = user_recommender.run_user_based_recommendation(
        n_movies_to_rate=15,
        top_similar_users=10,
        top_n_recommendations=10
    )
    
    return user_recommender, recommendations


if __name__ == "__main__":
    # Load data
    print("Loading data...")
    ratings = pd.read_csv(
        './data/ratings.dat',
        sep='::',
        engine='python',
        header=0,
        names=['user_id', 'movie_id', 'rating', 'timestamp'],
        encoding='ISO-8859-1'
    )
    
    movies = pd.read_csv(
        './data/movies.dat',
        sep='::',
        engine='python',
        header=0,
        names=['movie_id', 'title', 'genres'],
        encoding='ISO-8859-1'
    )
    
    # Run User-based Collaborative Filtering
    user_recommender, recommendations = main_user_based(ratings, movies)
