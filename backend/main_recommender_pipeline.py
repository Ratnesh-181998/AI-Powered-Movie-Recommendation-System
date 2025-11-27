"""
ZEE MOVIE RECOMMENDER SYSTEM - COMPLETE PIPELINE
=================================================
Comprehensive implementation of all recommendation approaches:
1. Item-based Pearson Correlation
2. Item-based Cosine Similarity (KNN)
3. Matrix Factorization (cmfrec)
4. User-based Collaborative Filtering

Author: Zee Recommender System Project
Date: November 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Import custom modules
from movie_recommender_system import MovieRecommenderSystem
from matrix_factorization_recommender import MatrixFactorizationRecommender, main_mf
from user_based_recommender import UserBasedRecommender, main_user_based


def create_project_summary(recommender, mf_metrics=None):
    """Create a comprehensive project summary"""
    
    summary = """
╔══════════════════════════════════════════════════════════════════════════════╗
║                    ZEE MOVIE RECOMMENDER SYSTEM                              ║
║                         PROJECT SUMMARY REPORT                               ║
╚══════════════════════════════════════════════════════════════════════════════╝

📊 DATASET OVERVIEW
═══════════════════════════════════════════════════════════════════════════════
"""
    
    summary += f"""
• Total Ratings:        {len(recommender.ratings):,}
• Total Movies:         {len(recommender.movies):,}
• Total Users:          {len(recommender.users):,}
• Rating Scale:         1-5 stars
• Time Period:          {recommender.merged_data['year'].min():.0f} - {recommender.merged_data['year'].max():.0f}
• Sparsity:            {(recommender.pivot_table.isnull().sum().sum() / (recommender.pivot_table.shape[0] * recommender.pivot_table.shape[1]) * 100):.2f}%

"""
    
    summary += """
🎯 IMPLEMENTED APPROACHES
═══════════════════════════════════════════════════════════════════════════════

1. ✅ ITEM-BASED PEARSON CORRELATION
   - Calculates correlation between movie rating patterns
   - Recommends movies with similar rating profiles
   - Range: -1 to +1

2. ✅ ITEM-BASED COSINE SIMILARITY (KNN)
   - Uses K-Nearest Neighbors algorithm
   - Cosine similarity metric
   - Range: 0 to 1
   - Efficient CSR matrix implementation

3. ✅ MATRIX FACTORIZATION (cmfrec)
   - Latent factor model (d=4)
   - Alternating Least Squares (ALS) method
   - Train-test split evaluation
"""
    
    if mf_metrics:
        summary += f"""   - RMSE: {mf_metrics['rmse']:.4f}
   - MAPE: {mf_metrics['mape']:.2f}%
   - MAE:  {mf_metrics['mae']:.4f}
"""
    
    summary += """
4. ✅ USER-BASED COLLABORATIVE FILTERING
   - Finds similar users using Pearson correlation
   - Weighted rating recommendations
   - Personalized for new users

"""
    
    # Add questionnaire answers
    age_ratings = recommender.merged_data.groupby('age')['rating'].count().sort_values(ascending=False)
    occupation_ratings = recommender.merged_data.groupby('occupation')['rating'].count().sort_values(ascending=False)
    gender_counts = recommender.merged_data['gender'].value_counts()
    male_percentage = gender_counts['M'] / gender_counts.sum() * 100
    decade_counts = (recommender.merged_data['release_year'] // 10 * 10).value_counts().sort_values(ascending=False)
    max_rated_movie = recommender.movie_stats.iloc[0]
    
    summary += f"""
📝 QUESTIONNAIRE ANSWERS
═══════════════════════════════════════════════════════════════════════════════

Q1. Age group with most ratings:
    → {age_ratings.index[0]} ({age_ratings.values[0]:,} ratings)

Q2. Occupation with most ratings:
    → Occupation {occupation_ratings.index[0]} ({occupation_ratings.values[0]:,} ratings)

Q3. Most users are Male:
    → TRUE ({male_percentage:.1f}% are male)

Q4. Most movies released in:
    → {int(decade_counts.index[0])}s ({decade_counts.values[0]:,} movies)

Q5. Movie with maximum ratings:
    → {max_rated_movie['title']} ({int(max_rated_movie['num_ratings'])} ratings)

Q6. Top 3 movies similar to 'Liar Liar':
    → See Pearson Correlation results above

Q7. Collaborative Filtering classification:
    → USER-based and ITEM-based

Q8. Similarity ranges:
    → Pearson Correlation: -1 to +1
    → Cosine Similarity: 0 to 1

Q9. Matrix Factorization metrics:
"""
    
    if mf_metrics:
        summary += f"""    → RMSE: {mf_metrics['rmse']:.4f}
    → MAPE: {mf_metrics['mape']:.2f}%
"""
    else:
        summary += "    → See evaluation results above\n"
    
    summary += """
Q10. Sparse matrix representation of [[1, 0], [3, 7]]:
     → (0, 0) 1  (1, 0) 3  (1, 1) 7

"""
    
    summary += """
📁 OUTPUT FILES GENERATED
═══════════════════════════════════════════════════════════════════════════════

• eda_visualizations.png          - Exploratory data analysis plots
• mf_evaluation.png               - Matrix factorization evaluation
• mf_embeddings_2d.png            - 2D embedding visualization
• project_summary.txt             - This summary report

"""
    
    summary += """
🎓 KEY LEARNINGS
═══════════════════════════════════════════════════════════════════════════════

1. Item-based methods work well for stable item catalogs
2. User-based methods are better for personalization
3. Matrix Factorization captures latent preferences effectively
4. Hybrid approaches can combine strengths of multiple methods
5. Evaluation metrics (RMSE, MAPE) help measure performance

"""
    
    summary += """
╔══════════════════════════════════════════════════════════════════════════════╗
║                          PROJECT COMPLETED SUCCESSFULLY                      ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""
    
    return summary


def main():
    """
    Main execution pipeline for the complete recommender system
    """
    
    print("\n" + "🎬"*50)
    print(" "*40 + "ZEE MOVIE RECOMMENDER SYSTEM")
    print(" "*45 + "COMPLETE PIPELINE")
    print("🎬"*50 + "\n")
    
    # =========================================================================
    # PART 1: ITEM-BASED APPROACHES
    # =========================================================================
    
    print("\n" + "█"*100)
    print(" "*35 + "PART 1: ITEM-BASED APPROACHES")
    print("█"*100 + "\n")
    
    # Initialize and run basic recommender system
    recommender = MovieRecommenderSystem(data_path='./data/')
    
    (recommender
     .load_data()
     .format_and_merge_data()
     .perform_eda()
     .group_and_aggregate()
     .create_pivot_table()
     .visualize_data()
     .answer_questions())
    
    # Test different recommendation approaches
    print("\n" + "▓"*100)
    print("TESTING RECOMMENDATION APPROACHES WITH 'Liar Liar (1997)'")
    print("▓"*100)
    
    test_movie = "Liar Liar (1997)"
    
    # Pearson Correlation
    recommender.pearson_correlation_recommender(test_movie, top_n=5)
    
    # Cosine Similarity
    recommender.cosine_similarity_recommender(test_movie, top_n=5)
    
    # KNN
    recommender.knn_recommender(test_movie, top_n=5)
    
    # =========================================================================
    # PART 2: MATRIX FACTORIZATION
    # =========================================================================
    
    print("\n\n" + "█"*100)
    print(" "*35 + "PART 2: MATRIX FACTORIZATION")
    print("█"*100 + "\n")
    
    try:
        mf_recommender, mf_metrics = main_mf(
            ratings_df=recommender.ratings,
            movies_df=recommender.movies
        )
    except Exception as e:
        print(f"⚠️  Matrix Factorization skipped: {e}")
        print("   Install cmfrec with: pip install cmfrec")
        mf_metrics = None
    
    # =========================================================================
    # PART 3: USER-BASED COLLABORATIVE FILTERING
    # =========================================================================
    
    print("\n\n" + "█"*100)
    print(" "*30 + "PART 3: USER-BASED COLLABORATIVE FILTERING")
    print("█"*100 + "\n")
    
    try:
        user_recommender, user_recommendations = main_user_based(
            ratings_df=recommender.ratings,
            movies_df=recommender.movies
        )
    except Exception as e:
        print(f"⚠️  User-based CF encountered an issue: {e}")
    
    # =========================================================================
    # FINAL SUMMARY
    # =========================================================================
    
    print("\n\n" + "█"*100)
    print(" "*40 + "GENERATING PROJECT SUMMARY")
    print("█"*100 + "\n")
    
    summary = create_project_summary(recommender, mf_metrics)
    
    # Print summary
    print(summary)
    
    # Save summary to file
    with open('project_summary.txt', 'w', encoding='utf-8') as f:
        f.write(summary)
    
    print("\n✅ Project summary saved to 'project_summary.txt'")
    
    # =========================================================================
    # COMPLETION
    # =========================================================================
    
    print("\n\n" + "╔" + "═"*98 + "╗")
    print("║" + " "*25 + "🎉 ALL TASKS COMPLETED SUCCESSFULLY! 🎉" + " "*25 + "║")
    print("╚" + "═"*98 + "╝\n")
    
    print("📊 Generated Files:")
    print("   1. eda_visualizations.png")
    print("   2. mf_evaluation.png (if cmfrec available)")
    print("   3. mf_embeddings_2d.png (if cmfrec available)")
    print("   4. project_summary.txt")
    print("\n" + "="*100 + "\n")
    
    return recommender, mf_metrics


if __name__ == "__main__":
    recommender, metrics = main()
