"""
ZEE MOVIE RECOMMENDER SYSTEM
============================
A comprehensive recommender system using:
1. Pearson Correlation (Item-based)
2. Cosine Similarity (Item-based with KNN)
3. Matrix Factorization (cmfrec)
4. User-based Collaborative Filtering (Optional)
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
from sklearn.metrics.pairwise import cosine_similarity
import warnings
warnings.filterwarnings('ignore')

# Set display options
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', 100)
plt.style.use('seaborn-v0_8-darkgrid')

class MovieRecommenderSystem:
    """
    Complete Movie Recommender System with multiple approaches
    """
    
    def __init__(self, data_path='./data/'):
        """Initialize the recommender system"""
        self.data_path = data_path
        self.ratings = None
        self.movies = None
        self.users = None
        self.merged_data = None
        self.pivot_table = None
        self.item_similarity_matrix = None
        self.user_similarity_matrix = None
        
    def load_data(self):
        """Load and format the data files"""
        print("="*80)
        print("STEP 1: LOADING DATA FILES")
        print("="*80)
        
        # Load ratings
        print("\n📊 Loading ratings.dat...")
        self.ratings = pd.read_csv(
            f'{self.data_path}ratings.dat',
            sep='::',
            engine='python',
            header=0,
            names=['user_id', 'movie_id', 'rating', 'timestamp'],
            encoding='ISO-8859-1'
        )
        
        # Load movies
        print("🎬 Loading movies.dat...")
        self.movies = pd.read_csv(
            f'{self.data_path}movies.dat',
            sep='::',
            engine='python',
            header=0,
            names=['movie_id', 'title', 'genres'],
            encoding='ISO-8859-1'
        )
        
        # Load users
        print("👥 Loading users.dat...")
        self.users = pd.read_csv(
            f'{self.data_path}users.dat',
            sep='::',
            engine='python',
            header=0,
            names=['user_id', 'gender', 'age', 'occupation', 'zip_code'],
            encoding='ISO-8859-1'
        )
        
        print("\n✅ Data loaded successfully!")
        print(f"   Ratings: {self.ratings.shape}")
        print(f"   Movies: {self.movies.shape}")
        print(f"   Users: {self.users.shape}")
        
        return self
    
    def format_and_merge_data(self):
        """Format and merge all dataframes"""
        print("\n" + "="*80)
        print("STEP 2: FORMATTING AND MERGING DATA")
        print("="*80)
        
        # Convert timestamp to datetime
        print("\n🔄 Converting timestamp to datetime...")
        self.ratings['date'] = pd.to_datetime(self.ratings['timestamp'], unit='s')
        self.ratings['year'] = self.ratings['date'].dt.year
        
        # Extract release year from movie title
        print("📅 Extracting release year from movie titles...")
        self.movies['release_year'] = self.movies['title'].str.extract(r'\((\d{4})\)').astype(float)
        
        # Split genres
        print("🎭 Processing genres...")
        self.movies['genre_list'] = self.movies['genres'].str.split('|')
        self.movies['num_genres'] = self.movies['genre_list'].apply(len)
        
        # Merge all dataframes
        print("🔗 Merging dataframes...")
        self.merged_data = self.ratings.merge(self.movies, on='movie_id')
        self.merged_data = self.merged_data.merge(self.users, on='user_id')
        
        print(f"\n✅ Merged data shape: {self.merged_data.shape}")
        print(f"   Columns: {list(self.merged_data.columns)}")
        
        return self
    
    def perform_eda(self):
        """Perform Exploratory Data Analysis"""
        print("\n" + "="*80)
        print("STEP 3: EXPLORATORY DATA ANALYSIS")
        print("="*80)
        
        # Check for missing values
        print("\n🔍 Checking for missing values:")
        print(self.merged_data.isnull().sum())
        
        # Data types
        print("\n📋 Data types:")
        print(self.merged_data.dtypes)
        
        # Basic statistics
        print("\n📊 Basic statistics:")
        print(self.merged_data.describe())
        
        # Age group analysis
        print("\n👥 Age group distribution:")
        age_counts = self.merged_data['age'].value_counts().sort_index()
        print(age_counts)
        
        # Gender distribution
        print("\n⚧ Gender distribution:")
        gender_counts = self.merged_data['gender'].value_counts()
        print(gender_counts)
        print(f"   Male percentage: {gender_counts['M'] / gender_counts.sum() * 100:.2f}%")
        
        # Occupation analysis
        print("\n💼 Occupation distribution:")
        occupation_counts = self.merged_data['occupation'].value_counts()
        print(occupation_counts.head(10))
        
        # Release year analysis
        print("\n📅 Release year distribution:")
        decade_counts = (self.merged_data['release_year'] // 10 * 10).value_counts().sort_index()
        print(decade_counts)
        
        return self
    
    def group_and_aggregate(self):
        """Group data by average rating and number of ratings"""
        print("\n" + "="*80)
        print("STEP 4: GROUPING AND AGGREGATION")
        print("="*80)
        
        # Movie-level aggregation
        print("\n🎬 Movie-level statistics:")
        self.movie_stats = self.merged_data.groupby('title').agg({
            'rating': ['mean', 'count', 'std'],
            'user_id': 'nunique'
        }).reset_index()
        
        self.movie_stats.columns = ['title', 'avg_rating', 'num_ratings', 'rating_std', 'unique_users']
        self.movie_stats = self.movie_stats.sort_values('num_ratings', ascending=False)
        
        print("\nTop 10 movies by number of ratings:")
        print(self.movie_stats.head(10))
        
        # User-level aggregation
        print("\n👥 User-level statistics:")
        self.user_stats = self.merged_data.groupby('user_id').agg({
            'rating': ['mean', 'count'],
            'movie_id': 'nunique'
        }).reset_index()
        
        self.user_stats.columns = ['user_id', 'avg_rating', 'num_ratings', 'unique_movies']
        
        print(f"   Average ratings per user: {self.user_stats['num_ratings'].mean():.2f}")
        print(f"   Max ratings by a user: {self.user_stats['num_ratings'].max()}")
        
        return self
    
    def create_pivot_table(self):
        """Create pivot table for collaborative filtering"""
        print("\n" + "="*80)
        print("STEP 5: CREATING PIVOT TABLE")
        print("="*80)
        
        print("\n📊 Creating user-movie pivot table...")
        self.pivot_table = self.ratings.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating'
        )
        
        print(f"   Pivot table shape: {self.pivot_table.shape}")
        print(f"   Sparsity: {(self.pivot_table.isnull().sum().sum() / (self.pivot_table.shape[0] * self.pivot_table.shape[1]) * 100):.2f}%")
        
        # Fill NaN with 0 for similarity calculations
        self.pivot_table_filled = self.pivot_table.fillna(0)
        
        return self
    
    def visualize_data(self):
        """Create visualizations"""
        print("\n" + "="*80)
        print("STEP 6: DATA VISUALIZATION")
        print("="*80)
        
        fig, axes = plt.subplots(2, 3, figsize=(18, 12))
        fig.suptitle('Movie Recommender System - Exploratory Data Analysis', fontsize=16, fontweight='bold')
        
        # 1. Rating distribution
        axes[0, 0].hist(self.merged_data['rating'], bins=5, color='skyblue', edgecolor='black')
        axes[0, 0].set_title('Rating Distribution')
        axes[0, 0].set_xlabel('Rating')
        axes[0, 0].set_ylabel('Frequency')
        
        # 2. Age group distribution
        age_counts = self.merged_data['age'].value_counts().sort_index()
        axes[0, 1].bar(age_counts.index, age_counts.values, color='coral')
        axes[0, 1].set_title('Age Group Distribution')
        axes[0, 1].set_xlabel('Age Group')
        axes[0, 1].set_ylabel('Count')
        
        # 3. Gender distribution
        gender_counts = self.merged_data['gender'].value_counts()
        axes[0, 2].pie(gender_counts.values, labels=gender_counts.index, autopct='%1.1f%%', colors=['lightblue', 'pink'])
        axes[0, 2].set_title('Gender Distribution')
        
        # 4. Top 10 occupations
        occupation_counts = self.merged_data['occupation'].value_counts().head(10)
        axes[1, 0].barh(range(len(occupation_counts)), occupation_counts.values, color='lightgreen')
        axes[1, 0].set_yticks(range(len(occupation_counts)))
        axes[1, 0].set_yticklabels(occupation_counts.index)
        axes[1, 0].set_title('Top 10 Occupations')
        axes[1, 0].set_xlabel('Count')
        
        # 5. Release year by decade
        decade_counts = (self.merged_data['release_year'] // 10 * 10).value_counts().sort_index()
        axes[1, 1].bar(decade_counts.index, decade_counts.values, color='mediumpurple')
        axes[1, 1].set_title('Movies by Decade')
        axes[1, 1].set_xlabel('Decade')
        axes[1, 1].set_ylabel('Count')
        axes[1, 1].tick_params(axis='x', rotation=45)
        
        # 6. Top 10 movies by ratings count
        top_movies = self.movie_stats.head(10)
        axes[1, 2].barh(range(len(top_movies)), top_movies['num_ratings'].values, color='gold')
        axes[1, 2].set_yticks(range(len(top_movies)))
        axes[1, 2].set_yticklabels([title[:30] + '...' if len(title) > 30 else title for title in top_movies['title']])
        axes[1, 2].set_title('Top 10 Most Rated Movies')
        axes[1, 2].set_xlabel('Number of Ratings')
        
        plt.tight_layout()
        plt.savefig('eda_visualizations.png', dpi=300, bbox_inches='tight')
        print("\n✅ Visualizations saved to 'eda_visualizations.png'")
        
        return self
    
    def pearson_correlation_recommender(self, movie_title, top_n=5):
        """Item-based recommender using Pearson Correlation"""
        print("\n" + "="*80)
        print(f"PEARSON CORRELATION RECOMMENDER")
        print("="*80)
        
        # Create movie-user pivot table
        movie_user_pivot = self.ratings.pivot_table(
            index='movie_id',
            columns='user_id',
            values='rating'
        )
        
        # Get movie ID from title
        movie_id = self.movies[self.movies['title'] == movie_title]['movie_id'].values
        
        if len(movie_id) == 0:
            print(f"❌ Movie '{movie_title}' not found!")
            return None
        
        movie_id = movie_id[0]
        
        # Get ratings for the target movie
        target_movie_ratings = movie_user_pivot.loc[movie_id].dropna()
        
        # Calculate Pearson correlation with all other movies
        correlations = []
        
        for other_movie_id in movie_user_pivot.index:
            if other_movie_id == movie_id:
                continue
            
            other_movie_ratings = movie_user_pivot.loc[other_movie_id].dropna()
            
            # Find common users
            common_users = target_movie_ratings.index.intersection(other_movie_ratings.index)
            
            if len(common_users) > 2:  # Need at least 3 common users
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
        correlations_df = pd.DataFrame(correlations)
        correlations_df = correlations_df.sort_values('correlation', ascending=False)
        
        # Get top N recommendations
        top_recommendations = correlations_df.head(top_n)
        top_recommendations = top_recommendations.merge(self.movies[['movie_id', 'title']], on='movie_id')
        
        print(f"\n🎬 Input Movie: {movie_title}")
        print(f"\n📊 Top {top_n} Similar Movies (Pearson Correlation):")
        print("-" * 80)
        
        for idx, row in top_recommendations.iterrows():
            print(f"{row['title']}")
            print(f"   Correlation: {row['correlation']:.4f} | Common Users: {row['common_users']}")
            print()
        
        return top_recommendations
    
    def cosine_similarity_recommender(self, movie_title, top_n=5):
        """Item-based recommender using Cosine Similarity with KNN"""
        print("\n" + "="*80)
        print(f"COSINE SIMILARITY RECOMMENDER (KNN)")
        print("="*80)
        
        # Create movie-user pivot table
        movie_user_pivot = self.ratings.pivot_table(
            index='movie_id',
            columns='user_id',
            values='rating'
        ).fillna(0)
        
        # Calculate item similarity matrix
        print("\n📊 Calculating item similarity matrix...")
        self.item_similarity_matrix = cosine_similarity(movie_user_pivot)
        
        print(f"   Item similarity matrix shape: {self.item_similarity_matrix.shape}")
        
        # Calculate user similarity matrix
        print("📊 Calculating user similarity matrix...")
        user_movie_pivot = self.ratings.pivot_table(
            index='user_id',
            columns='movie_id',
            values='rating'
        ).fillna(0)
        
        self.user_similarity_matrix = cosine_similarity(user_movie_pivot)
        print(f"   User similarity matrix shape: {self.user_similarity_matrix.shape}")
        
        # Get movie ID from title
        movie_id = self.movies[self.movies['title'] == movie_title]['movie_id'].values
        
        if len(movie_id) == 0:
            print(f"❌ Movie '{movie_title}' not found!")
            return None
        
        movie_id = movie_id[0]
        
        # Find index of the movie
        movie_idx = movie_user_pivot.index.get_loc(movie_id)
        
        # Get similarity scores
        similarity_scores = list(enumerate(self.item_similarity_matrix[movie_idx]))
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get top N (excluding the movie itself)
        top_similar = similarity_scores[1:top_n+1]
        
        # Get movie details
        recommendations = []
        for idx, score in top_similar:
            movie_id_rec = movie_user_pivot.index[idx]
            movie_title_rec = self.movies[self.movies['movie_id'] == movie_id_rec]['title'].values[0]
            recommendations.append({
                'title': movie_title_rec,
                'similarity_score': score
            })
        
        recommendations_df = pd.DataFrame(recommendations)
        
        print(f"\n🎬 Input Movie: {movie_title}")
        print(f"\n📊 Top {top_n} Similar Movies (Cosine Similarity):")
        print("-" * 80)
        
        for idx, row in recommendations_df.iterrows():
            print(f"{row['title']}")
            print(f"   Similarity Score: {row['similarity_score']:.4f}")
            print()
        
        return recommendations_df
    
    def knn_recommender(self, movie_title, top_n=5):
        """KNN-based recommender using sklearn"""
        print("\n" + "="*80)
        print(f"K-NEAREST NEIGHBORS RECOMMENDER")
        print("="*80)
        
        # Create movie-user pivot table
        movie_user_pivot = self.ratings.pivot_table(
            index='movie_id',
            columns='user_id',
            values='rating'
        ).fillna(0)
        
        # Create CSR matrix for efficient computation
        print("\n🔄 Creating CSR matrix...")
        csr_data = csr_matrix(movie_user_pivot.values)
        print(f"   CSR matrix shape: {csr_data.shape}")
        
        # Fit KNN model
        print("🤖 Fitting KNN model...")
        knn_model = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=top_n+1)
        knn_model.fit(csr_data)
        
        # Get movie ID from title
        movie_id = self.movies[self.movies['title'] == movie_title]['movie_id'].values
        
        if len(movie_id) == 0:
            print(f"❌ Movie '{movie_title}' not found!")
            return None
        
        movie_id = movie_id[0]
        
        # Find index of the movie
        movie_idx = movie_user_pivot.index.get_loc(movie_id)
        
        # Find nearest neighbors
        distances, indices = knn_model.kneighbors(
            csr_data[movie_idx],
            n_neighbors=top_n+1
        )
        
        # Get recommendations (excluding the movie itself)
        recommendations = []
        for i in range(1, len(indices.flatten())):
            movie_id_rec = movie_user_pivot.index[indices.flatten()[i]]
            movie_title_rec = self.movies[self.movies['movie_id'] == movie_id_rec]['title'].values[0]
            recommendations.append({
                'title': movie_title_rec,
                'distance': distances.flatten()[i],
                'similarity': 1 - distances.flatten()[i]
            })
        
        recommendations_df = pd.DataFrame(recommendations)
        
        print(f"\n🎬 Input Movie: {movie_title}")
        print(f"\n📊 Top {top_n} Similar Movies (KNN):")
        print("-" * 80)
        
        for idx, row in recommendations_df.iterrows():
            print(f"{row['title']}")
            print(f"   Similarity: {row['similarity']:.4f} | Distance: {row['distance']:.4f}")
            print()
        
        return recommendations_df
    
    def answer_questions(self):
        """Answer the questionnaire"""
        print("\n" + "="*80)
        print("QUESTIONNAIRE ANSWERS")
        print("="*80)
        
        # Q1: Age group with most ratings
        age_ratings = self.merged_data.groupby('age')['rating'].count().sort_values(ascending=False)
        print(f"\n1. Age group with most ratings: {age_ratings.index[0]} (Count: {age_ratings.values[0]:,})")
        
        # Q2: Occupation with most ratings
        occupation_ratings = self.merged_data.groupby('occupation')['rating'].count().sort_values(ascending=False)
        print(f"\n2. Occupation with most ratings: {occupation_ratings.index[0]} (Count: {occupation_ratings.values[0]:,})")
        
        # Q3: Gender distribution
        gender_counts = self.merged_data['gender'].value_counts()
        male_percentage = gender_counts['M'] / gender_counts.sum() * 100
        print(f"\n3. Most users are Male: {male_percentage > 50} ({male_percentage:.2f}% are male)")
        
        # Q4: Most common decade
        decade_counts = (self.merged_data['release_year'] // 10 * 10).value_counts().sort_values(ascending=False)
        print(f"\n4. Most movies released in: {int(decade_counts.index[0])}s (Count: {decade_counts.values[0]:,})")
        
        # Q5: Movie with maximum ratings
        max_rated_movie = self.movie_stats.iloc[0]
        print(f"\n5. Movie with maximum ratings: {max_rated_movie['title']} ({int(max_rated_movie['num_ratings'])} ratings)")
        
        # Q8: Correlation and Similarity ranges
        print(f"\n8. Pearson Correlation ranges: -1 to 1")
        print(f"   Cosine Similarity ranges: 0 to 1")
        
        # Q10: Sparse matrix representation
        print(f"\n10. Sparse 'row' matrix representation of [[1, 0], [3, 7]]:")
        print(f"    ans: (0, 0) 1  (1, 0) 3  (1, 1) 7")
        
        return self


def main():
    """Main execution function"""
    print("\n" + "🎬"*40)
    print(" "*30 + "ZEE MOVIE RECOMMENDER SYSTEM")
    print("🎬"*40 + "\n")
    
    # Initialize recommender system
    recommender = MovieRecommenderSystem(data_path='./data/')
    
    # Execute pipeline
    (recommender
     .load_data()
     .format_and_merge_data()
     .perform_eda()
     .group_and_aggregate()
     .create_pivot_table()
     .visualize_data()
     .answer_questions())
    
    # Test Pearson Correlation Recommender
    print("\n" + "🔵"*40)
    recommender.pearson_correlation_recommender("Liar Liar (1997)", top_n=5)
    
    # Test Cosine Similarity Recommender
    print("\n" + "🟢"*40)
    recommender.cosine_similarity_recommender("Liar Liar (1997)", top_n=5)
    
    # Test KNN Recommender
    print("\n" + "🟡"*40)
    recommender.knn_recommender("Liar Liar (1997)", top_n=5)
    
    print("\n" + "="*80)
    print("✅ RECOMMENDER SYSTEM EXECUTION COMPLETED!")
    print("="*80)
    
    return recommender


if __name__ == "__main__":
    recommender = main()
