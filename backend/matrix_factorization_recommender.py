"""
MATRIX FACTORIZATION RECOMMENDER
=================================
Using cmfrec library for collaborative filtering with matrix factorization
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

try:
    import cmfrec
    CMFREC_AVAILABLE = True
except ImportError:
    CMFREC_AVAILABLE = False
    print("⚠️  cmfrec not installed. Install with: pip install cmfrec")


class MatrixFactorizationRecommender:
    """
    Matrix Factorization based Recommender System
    """
    
    def __init__(self, ratings_df, movies_df, n_factors=4):
        """
        Initialize Matrix Factorization Recommender
        
        Parameters:
        -----------
        ratings_df : DataFrame with columns [user_id, movie_id, rating]
        movies_df : DataFrame with columns [movie_id, title, genres]
        n_factors : Number of latent factors (d)
        """
        self.ratings = ratings_df
        self.movies = movies_df
        self.n_factors = n_factors
        self.model = None
        self.user_factors = None
        self.item_factors = None
        
    def train_test_split_data(self, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        print("\n" + "="*80)
        print("TRAIN-TEST SPLIT")
        print("="*80)
        
        train_data, test_data = train_test_split(
            self.ratings,
            test_size=test_size,
            random_state=random_state
        )
        
        print(f"\n📊 Train set size: {len(train_data):,} ({(1-test_size)*100:.0f}%)")
        print(f"📊 Test set size: {len(test_data):,} ({test_size*100:.0f}%)")
        
        return train_data, test_data
    
    def train_model(self, train_data=None):
        """Train Matrix Factorization model using cmfrec"""
        print("\n" + "="*80)
        print(f"TRAINING MATRIX FACTORIZATION MODEL (d={self.n_factors})")
        print("="*80)
        
        if not CMFREC_AVAILABLE:
            print("❌ cmfrec library not available!")
            return None
        
        if train_data is None:
            train_data = self.ratings
        
        print(f"\n🤖 Training model with {len(train_data):,} ratings...")
        print(f"   Latent factors (d): {self.n_factors}")
        
        # Create model
        self.model = cmfrec.CMF(
            k=self.n_factors,
            lambda_=0.1,
            method='als',
            verbose=False,
            random_state=42
        )
        
        # Fit model
        self.model.fit(
            X=train_data[['user_id', 'movie_id', 'rating']].values
        )
        
        # Extract factors
        self.user_factors = self.model.A_  # User embeddings
        self.item_factors = self.model.B_  # Item embeddings
        
        print(f"\n✅ Model trained successfully!")
        print(f"   User factors shape: {self.user_factors.shape}")
        print(f"   Item factors shape: {self.item_factors.shape}")
        
        return self
    
    def evaluate_model(self, test_data):
        """Evaluate model using RMSE and MAPE"""
        print("\n" + "="*80)
        print("MODEL EVALUATION")
        print("="*80)
        
        if self.model is None:
            print("❌ Model not trained yet!")
            return None
        
        # Make predictions
        predictions = []
        actuals = []
        
        for _, row in test_data.iterrows():
            try:
                pred = self.model.predict(
                    user=[row['user_id']],
                    item=[row['movie_id']]
                )[0]
                predictions.append(pred)
                actuals.append(row['rating'])
            except:
                continue
        
        predictions = np.array(predictions)
        actuals = np.array(actuals)
        
        # Calculate RMSE
        rmse = np.sqrt(np.mean((predictions - actuals) ** 2))
        
        # Calculate MAPE
        mape = np.mean(np.abs((actuals - predictions) / actuals)) * 100
        
        # Calculate MAE
        mae = np.mean(np.abs(predictions - actuals))
        
        print(f"\n📊 Evaluation Metrics:")
        print(f"   RMSE: {rmse:.4f}")
        print(f"   MAPE: {mape:.2f}%")
        print(f"   MAE:  {mae:.4f}")
        
        # Create evaluation plot
        fig, axes = plt.subplots(1, 2, figsize=(14, 5))
        
        # Scatter plot
        axes[0].scatter(actuals, predictions, alpha=0.5, s=10)
        axes[0].plot([actuals.min(), actuals.max()], 
                     [actuals.min(), actuals.max()], 
                     'r--', lw=2, label='Perfect Prediction')
        axes[0].set_xlabel('Actual Ratings')
        axes[0].set_ylabel('Predicted Ratings')
        axes[0].set_title(f'Actual vs Predicted Ratings\nRMSE: {rmse:.4f}')
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)
        
        # Error distribution
        errors = predictions - actuals
        axes[1].hist(errors, bins=50, color='skyblue', edgecolor='black', alpha=0.7)
        axes[1].axvline(0, color='red', linestyle='--', linewidth=2, label='Zero Error')
        axes[1].set_xlabel('Prediction Error')
        axes[1].set_ylabel('Frequency')
        axes[1].set_title(f'Error Distribution\nMAPE: {mape:.2f}%')
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.savefig('mf_evaluation.png', dpi=300, bbox_inches='tight')
        print(f"\n✅ Evaluation plot saved to 'mf_evaluation.png'")
        
        return {'rmse': rmse, 'mape': mape, 'mae': mae}
    
    def get_item_recommendations_mf(self, movie_title, top_n=5):
        """Get item-item recommendations using MF embeddings"""
        print("\n" + "="*80)
        print(f"ITEM-ITEM SIMILARITY (MF Embeddings, d={self.n_factors})")
        print("="*80)
        
        if self.model is None:
            print("❌ Model not trained yet!")
            return None
        
        # Get movie ID
        movie_id = self.movies[self.movies['title'] == movie_title]['movie_id'].values
        
        if len(movie_id) == 0:
            print(f"❌ Movie '{movie_title}' not found!")
            return None
        
        movie_id = movie_id[0]
        
        # Get movie index in the model
        try:
            movie_idx = np.where(self.model.item_mapping_ == movie_id)[0][0]
        except:
            print(f"❌ Movie not in training data!")
            return None
        
        # Get movie embedding
        movie_embedding = self.item_factors[movie_idx]
        
        # Calculate cosine similarity with all other movies
        similarities = np.dot(self.item_factors, movie_embedding) / (
            np.linalg.norm(self.item_factors, axis=1) * np.linalg.norm(movie_embedding)
        )
        
        # Get top N similar movies (excluding the movie itself)
        similar_indices = np.argsort(similarities)[::-1][1:top_n+1]
        
        # Get movie details
        recommendations = []
        for idx in similar_indices:
            similar_movie_id = self.model.item_mapping_[idx]
            similar_movie_title = self.movies[self.movies['movie_id'] == similar_movie_id]['title'].values[0]
            recommendations.append({
                'title': similar_movie_title,
                'similarity': similarities[idx]
            })
        
        recommendations_df = pd.DataFrame(recommendations)
        
        print(f"\n🎬 Input Movie: {movie_title}")
        print(f"\n📊 Top {top_n} Similar Movies (MF Embeddings):")
        print("-" * 80)
        
        for idx, row in recommendations_df.iterrows():
            print(f"{row['title']}")
            print(f"   Similarity: {row['similarity']:.4f}")
            print()
        
        return recommendations_df
    
    def get_user_recommendations_mf(self, user_id, top_n=10):
        """Get user recommendations using MF embeddings"""
        print("\n" + "="*80)
        print(f"USER RECOMMENDATIONS (MF Embeddings, d={self.n_factors})")
        print("="*80)
        
        if self.model is None:
            print("❌ Model not trained yet!")
            return None
        
        # Get user index
        try:
            user_idx = np.where(self.model.user_mapping_ == user_id)[0][0]
        except:
            print(f"❌ User {user_id} not in training data!")
            return None
        
        # Get user embedding
        user_embedding = self.user_factors[user_idx]
        
        # Calculate predicted ratings for all items
        predicted_ratings = np.dot(self.item_factors, user_embedding)
        
        # Get movies the user has already rated
        user_rated_movies = self.ratings[self.ratings['user_id'] == user_id]['movie_id'].values
        
        # Get top N unrated movies
        recommendations = []
        for idx in np.argsort(predicted_ratings)[::-1]:
            movie_id = self.model.item_mapping_[idx]
            
            if movie_id not in user_rated_movies:
                movie_title = self.movies[self.movies['movie_id'] == movie_id]['title'].values[0]
                recommendations.append({
                    'title': movie_title,
                    'predicted_rating': predicted_ratings[idx]
                })
                
                if len(recommendations) >= top_n:
                    break
        
        recommendations_df = pd.DataFrame(recommendations)
        
        print(f"\n👤 User ID: {user_id}")
        print(f"\n📊 Top {top_n} Recommended Movies:")
        print("-" * 80)
        
        for idx, row in recommendations_df.iterrows():
            print(f"{idx+1}. {row['title']}")
            print(f"   Predicted Rating: {row['predicted_rating']:.2f}")
            print()
        
        return recommendations_df
    
    def visualize_embeddings_2d(self, n_movies=100):
        """Visualize movie embeddings in 2D"""
        print("\n" + "="*80)
        print("EMBEDDING VISUALIZATION (d=2)")
        print("="*80)
        
        # Train a new model with d=2 for visualization
        print("\n🤖 Training model with d=2 for visualization...")
        
        model_2d = cmfrec.CMF(
            k=2,
            lambda_=0.1,
            method='als',
            verbose=False,
            random_state=42
        )
        
        model_2d.fit(
            X=self.ratings[['user_id', 'movie_id', 'rating']].values
        )
        
        item_factors_2d = model_2d.B_
        
        # Get top N most rated movies for visualization
        movie_counts = self.ratings['movie_id'].value_counts().head(n_movies)
        top_movie_ids = movie_counts.index.tolist()
        
        # Filter embeddings for top movies
        embeddings_to_plot = []
        labels = []
        
        for movie_id in top_movie_ids:
            try:
                movie_idx = np.where(model_2d.item_mapping_ == movie_id)[0][0]
                embeddings_to_plot.append(item_factors_2d[movie_idx])
                movie_title = self.movies[self.movies['movie_id'] == movie_id]['title'].values[0]
                labels.append(movie_title[:30])  # Truncate long titles
            except:
                continue
        
        embeddings_to_plot = np.array(embeddings_to_plot)
        
        # Create visualization
        plt.figure(figsize=(16, 12))
        scatter = plt.scatter(
            embeddings_to_plot[:, 0],
            embeddings_to_plot[:, 1],
            c=range(len(embeddings_to_plot)),
            cmap='viridis',
            s=100,
            alpha=0.6,
            edgecolors='black',
            linewidth=0.5
        )
        
        # Add labels for some movies
        for i in range(min(20, len(labels))):
            plt.annotate(
                labels[i],
                (embeddings_to_plot[i, 0], embeddings_to_plot[i, 1]),
                fontsize=8,
                alpha=0.7
            )
        
        plt.xlabel('Latent Factor 1', fontsize=12)
        plt.ylabel('Latent Factor 2', fontsize=12)
        plt.title(f'Movie Embeddings Visualization (d=2)\nTop {n_movies} Most Rated Movies', 
                  fontsize=14, fontweight='bold')
        plt.colorbar(scatter, label='Movie Index')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('mf_embeddings_2d.png', dpi=300, bbox_inches='tight')
        
        print(f"\n✅ 2D embedding visualization saved to 'mf_embeddings_2d.png'")
        print(f"\n📊 Analysis:")
        print(f"   - Movies closer together in the embedding space are more similar")
        print(f"   - The two latent factors capture different aspects of movie preferences")
        print(f"   - Clusters may represent different genres or movie characteristics")
        
        return embeddings_to_plot, labels


def main_mf(ratings_df, movies_df):
    """Main function for Matrix Factorization"""
    print("\n" + "🎯"*40)
    print(" "*25 + "MATRIX FACTORIZATION RECOMMENDER")
    print("🎯"*40 + "\n")
    
    if not CMFREC_AVAILABLE:
        print("❌ Please install cmfrec: pip install cmfrec")
        return None
    
    # Initialize recommender with d=4
    mf_recommender = MatrixFactorizationRecommender(
        ratings_df=ratings_df,
        movies_df=movies_df,
        n_factors=4
    )
    
    # Train-test split
    train_data, test_data = mf_recommender.train_test_split_data(test_size=0.2)
    
    # Train model
    mf_recommender.train_model(train_data)
    
    # Evaluate model
    metrics = mf_recommender.evaluate_model(test_data)
    
    # Item-item recommendations using MF embeddings
    mf_recommender.get_item_recommendations_mf("Liar Liar (1997)", top_n=5)
    
    # User recommendations
    mf_recommender.get_user_recommendations_mf(user_id=1, top_n=10)
    
    # Visualize embeddings in 2D
    mf_recommender.visualize_embeddings_2d(n_movies=100)
    
    print("\n" + "="*80)
    print("✅ MATRIX FACTORIZATION COMPLETED!")
    print("="*80)
    
    return mf_recommender, metrics


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
    
    # Run Matrix Factorization
    mf_recommender, metrics = main_mf(ratings, movies)
